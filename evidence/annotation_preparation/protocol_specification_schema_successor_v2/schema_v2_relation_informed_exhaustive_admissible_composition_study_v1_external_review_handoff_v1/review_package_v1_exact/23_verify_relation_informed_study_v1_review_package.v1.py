#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "01_study_v1.EXACT_COPY.json":
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",

    "02_exhaustiveness_accounting.EXACT_COPY.json":
        "ae56e06b6668c301167efdd7e81ba937848446215b49be52d1268c69a2c5d643",

    "03_study_report.EXACT_COPY.md":
        "d0de61d7285ae8ba2c3ff2fcf2048f8c8dca145f87929a93262ab26c2e4b2642",

    "04_decision0102_a02_final_output.EXACT_COPY.txt":
        "82cd248d4d323b691c8635ba9d1b992dfe4dbe0de7033b7a9eb92f0f4ce4bb50",

    "05_decision0102_a02_consumption_record.EXACT_COPY.json":
        "022a8c1fa5f6630261a91e815c1c9339037188b103ae97634a8b7a48c03a2753",

    "06_study_safe_verifier.EXACT_COPY.py":
        "b0ff1cb58eee830aa97c2759b54c78a96c9190c3c173a59483ee459bce8e8d22",

    "07_study_checksum_manifest.EXACT_COPY.SHA256SUMS":
        "aa58e9221db7fa0c2bc17b2831e051ce6d7574c000d35d4f92c26ae923340140",

    "08_decision0103.EXACT_COPY.md":
        "75d962331741137325f32af5826ac07f3aa1d67914c896b629f8213974b2087f",

    "09_decision0102_authorization_record.EXACT_COPY.json":
        "c0370ce7e52c7dfb74e375c1a5885119f5b086be759027dc8ae09d9db80c628d",

    "10_decision0102_a02.RETIRED_EXACT_COPY.py":
        "6781df3a0b4fcf1c8bc2ce59b7f017106ce2a158d15e68cf5557781532f77af2",

    "11_decision0102_authorization_checksum.EXACT_COPY.SHA256SUMS":
        "949938100623931a3146beefa49fdfa4c6c2cd7eeaeb9249fe19843fb629e15c",

    "12_active_schema_v2.EXACT_COPY.json":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "13_relation_artifact.EXACT_COPY.json":
        "239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32",

    "14_traceability_artifact.EXACT_COPY.json":
        "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4",

    "15_decision0104_review_package_authorization_record.EXACT_COPY.json":
        "1e2e8ab6752cf720345ebc0151cd4ed561cf84a82f73dc9cbcfec36eaaeb82cf",

    "16_decision0104_a02.RETIRED_EXACT_COPY.py":
        "f656d264d1ec42f059c4dae2d3ee8dba79949d2aa583f3a58ee426bee896b4b0",

    "17_decision0104_authorization_checksum.EXACT_COPY.SHA256SUMS":
        "b3707447d2a09b348e8346c96d122d997e768f3945eec2f2ab4ccd8991b9c6a7",

    "20_decision0104.EXACT_COPY.md":
        "410fc3450d2b3edb604bab7e2ad59fb7643e48f63da3304f4ab86a4430f3df53",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + path.name)

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

# ------------------------------------------------------------
# Critical immutable bindings.
# ------------------------------------------------------------

for name, expected in FILES.items():
    path = HERE / name

    if sha(path) != expected:
        fail(
            "SOURCE_SHA|"
            + name
        )

# ------------------------------------------------------------
# Study semantics.
# ------------------------------------------------------------

study = json.loads(
    (HERE / "01_study_v1.EXACT_COPY.json").read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail("GLOBAL_OUTCOME")

if study["relation_classification_totals"] != {
    "SEMANTICALLY_RELATED": 113,
    "NOT_SEMANTICALLY_RELATED": 969,
    "UNRESOLVED": 8665,
}:
    fail("RELATION_TOTALS")

b = study["approved_input_bindings"]

if b["relation_pair_count"] != 9747:
    fail("RELATION_PAIR_COUNT")

if b["matrix_field_class_count"] != 57:
    fail("MATRIX_FIELD_CLASS_COUNT")

if b["schema_v2_property_path_count"] != 171:
    fail("SCHEMA_PATH_COUNT")

if b["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if b["source_leaf_record_count"] != 531:
    fail("LEAF_RECORD_COUNT")

if len(
    study["losslessness_requirement_results"]
) != 17:
    fail("REQUIREMENT_COUNT")

a = study["exhaustiveness_accounting"]

if a[
    "whole_v4_admissible_composition_universe_proven_complete"
] is not False:
    fail("WHOLE_V4_EXHAUSTIVENESS_OVERCLAIM")

r = study["admissibility_rules"]

if r[
    "matrix_and_unit_field_class_vocabularies_equated"
] is not False:
    fail("FIELD_CLASS_VOCABULARIES_EQUATED")

if r["unresolved"] != \
        "NOT_AUTOMATICALLY_POSITIVE":
    fail("UNRESOLVED_POLICY")

# ------------------------------------------------------------
# Old Decision-0102 A02 remains retired.
# ------------------------------------------------------------

old_consumption = json.loads(
    (
        HERE
        / "05_decision0102_a02_consumption_record.EXACT_COPY.json"
    ).read_text(
        encoding="utf-8"
    )
)

if old_consumption[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail("OLD_A02_RETIREMENT")

if old_consumption[
    "must_never_be_rerun"
] is not True:
    fail("OLD_A02_RERUN_GUARD")

# ------------------------------------------------------------
# Decision-0104 A02 final output and retirement.
# ------------------------------------------------------------

new_consumption = json.loads(
    (
        HERE
        / "19_decision0104_a02_consumption_record.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if new_consumption["final_run_result"] != "PASS":
    fail("NEW_A02_FINAL_RUN")

if new_consumption[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail("NEW_A02_RETIREMENT")

if new_consumption[
    "must_never_be_rerun"
] is not True:
    fail("NEW_A02_RERUN_GUARD")

new_output = (
    HERE
    / "18_decision0104_a02_final_output.EXACT_COPY.txt"
)

if sha(new_output) != \
        new_consumption["final_output_sha256"]:
    fail("NEW_A02_OUTPUT_SHA")

if new_output.stat().st_size != \
        new_consumption["final_output_size_bytes"]:
    fail("NEW_A02_OUTPUT_SIZE")

if (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
    not in new_output.read_text(encoding="utf-8")
):
    fail("NEW_A02_PASS_MARKER")

# ------------------------------------------------------------
# Blank reviewer packet.
# ------------------------------------------------------------

packet = (
    HERE
    / "21_RIAC01_RIAC08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

text = packet.read_text(
    encoding="utf-8"
)

for rid in (
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
):
    section = re.search(
        rf"^## {rid} — .*?"
        rf"(?=^## RIAC\d{{2}} —|^# Overall review decision)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail("REVIEW_ITEM|" + rid)

    body = section.group(0)

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        body,
        flags=re.MULTILINE,
    ):
        fail("ITEM_DECISION_NOT_BLANK|" + rid)

    if not re.search(
        r"^Reviewer notes:[ \t]*$",
        body,
        flags=re.MULTILINE,
    ):
        fail("ITEM_NOTES_NOT_BLANK|" + rid)

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail("OVERALL_DECISION_NOT_BLANK")

for prefix in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    values = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if values != [""]:
        fail("REVIEWER_IDENTITY_PREPOPULATED|" + prefix)

if "Reviewer role: Spec-Technical-Reviewer-1" not in text:
    fail("REVIEWER_ROLE")

# ------------------------------------------------------------
# Package manifest.
# ------------------------------------------------------------

manifest_path = (
    HERE
    / "22_review_package_manifest.v1.json"
)

manifest = json.loads(
    manifest_path.read_text(
        encoding="utf-8"
    )
)

if manifest["package_state"] != \
        "BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW":
    fail("PACKAGE_STATE")

if manifest["review_target"] != \
        "Schema-V2 Relation-Informed Exhaustive Admissible Composition Study V1":
    fail("REVIEW_TARGET")

if manifest["study_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail("MANIFEST_STUDY_OUTCOME")

if manifest["required_reviewer_role"] != \
        "Spec-Technical-Reviewer-1":
    fail("MANIFEST_REVIEWER_ROLE")

entries = manifest["files"]

if len(entries) != 22:
    fail(
        "MANIFEST_ENTRY_COUNT|"
        + str(len(entries))
    )

seen = set()

for entry in entries:
    name = entry["name"]

    if name in seen:
        fail("MANIFEST_DUPLICATE|" + name)

    seen.add(name)

    path = HERE / name

    if sha(path) != entry["sha256"]:
        fail("MANIFEST_SHA|" + name)

    if path.stat().st_size != entry["size_bytes"]:
        fail("MANIFEST_SIZE|" + name)

# ------------------------------------------------------------
# Full package checksum closure.
# ------------------------------------------------------------

sums = (
    HERE
    / "24_review_package.v1.SHA256SUMS"
)

if sums.is_file():
    lines = [
        x
        for x in sums.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    if len(lines) != 23:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        path = HERE / rel

        if sha(path) != digest:
            fail("CHECKSUM|" + rel)

print("STUDY_V1_EXACT_BINDING=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("RELATION_PAIR_COUNT=9747")
print("SEMANTIC_UNIT_COUNT=109")
print("LOSSLESSNESS_REQUIREMENT_COUNT=17")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_UNIVERSE_PROVEN_COMPLETE=NO")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0102_A02_EXECUTED_BY_PACKAGE_VERIFIER=NO")

print("DECISION_0104_A02_FINAL_SUCCESSFUL_RUN_RECORDED=YES")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_EXECUTED_BY_PACKAGE_VERIFIER=NO")

print("RIAC01_RIAC08_PRESENT=YES")
print("REVIEWER_ITEM_DECISIONS_PREPOPULATED=NO")
print("REVIEWER_NOTES_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("OVERALL_REVIEW_DECISION_PREPOPULATED=NO")

print("REVIEW_PACKAGE_STATE=BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW")

print("STUDY_GOVERNANCE_ADOPTED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SELF_CONTAINED_RELATION_INFORMED_STUDY_V1_REVIEW_PACKAGE=PASS")
