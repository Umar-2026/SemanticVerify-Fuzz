#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "v2_json": HERE / "01_corrective_assessment_v2.EXACT_COPY.json",
    "v2_md": HERE / "02_corrective_assessment_v2.EXACT_COPY.md",
    "v2_sums": HERE / "03_corrective_assessment_v2_checksums.EXACT_COPY.SHA256SUMS",
    "decision0079": HERE / "04_decision_0079_author_checkpoint.EXACT_COPY.md",
    "auth0080": HERE / "05_decision_0080_review_package_authorization.EXACT_COPY.json",
    "decision0080": HERE / "06_decision_0080.EXACT_COPY.md",
    "v1_review": HERE / "07_completed_assessment_v1_human_review.EXACT_COPY.md",
    "v1_review_record": HERE / "08_assessment_v1_human_review_record.EXACT_COPY.json",
    "v1_json": HERE / "09_assessment_v1.EXACT_COPY.json",
    "v1_md": HERE / "10_assessment_v1.EXACT_COPY.md",
    "proof": HERE / "11_residual_schema_v2_insufficiency_proof.EXACT_COPY.json",
    "v4": HERE / "12_curl_technical_protocol_working_draft_v4.EXACT_COPY.json",
    "schema_v2": HERE / "13_active_protocol_specification_v2_schema.EXACT_COPY.json",
    "evidence": HERE / "14_corrective_v2_review_evidence.v1.json",
    "packet": HERE / "15_corrective_v2_reviewer_packet.REVIEW_DRAFT.v1.md",
    "manifest": HERE / "17_corrective_v2_review_package_manifest.v1.json",
}

EXPECTED = {
    "v2_json": "94e056db6a2b9eb993b4cea379491dbc69bc528115b755704b2ff587580b55dc",
    "v2_md": "e54d8ea0039c87a33ae4d07593428ac1d003bf7648fe9511d12fee5d35d1bd30",
    "v2_sums": "d606edaa2229b20b3f43012bcf669bb107ba0136812dbdfa44ca45e7c492072a",
    "decision0079": "3f2ffbba2bebf33f749fab1d0b3403c5b12aaff5e747c4b367c17694ad9bd742",
    "auth0080": "9cba113bbd03641acca9608ab1f63a60736a6d9211f6dd7551fe0a9642f61fb8",
    "decision0080": "3e46e63bf409b747b0b4be36dc2445d5a9a611dd527aa47185849e114af04fa8",
    "v1_review": "e81cf41aa331e371541cb3b3c8b9392e66ccedbf8b87a3e9ed3943dee8a5fd22",
    "v1_json": "be64ed3755b5c1a525c23e5e6b1472a35b84a5b3640ce22990dbceb5a41bdb70",
    "v1_md": "1137858f4da8cdfaaa7b88332f581f810f9f286f7b4ca71530b186abfc884008",
    "proof": "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",
    "v4": "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8",
    "schema_v2": "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + path.name)

    return hashlib.sha256(path.read_bytes()).hexdigest()

for key, expected in EXPECTED.items():
    if sha(FILES[key]) != expected:
        fail("EXACT_COPY_SHA|" + key)

v2 = json.loads(FILES["v2_json"].read_text(encoding="utf-8"))
review_record = json.loads(
    FILES["v1_review_record"].read_text(encoding="utf-8")
)
evidence = json.loads(
    FILES["evidence"].read_text(encoding="utf-8")
)

if v2[
    "current_governance_conclusion"
]["selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("V2_OUTCOME")

if v2[
    "CV2_SR02_correction"
]["corrected_distinction"]["proposition_A_supported"] is not True:
    fail("PROP_A")

if v2[
    "CV2_SR02_correction"
]["corrected_distinction"]["proposition_B_supported"] is not False:
    fail("PROP_B")

if v2[
    "CV2_SR02_correction"
]["semantically_related_multifield_schema_v2_compositions_exhaustively_assessed"] is not False:
    fail("MULTIFIELD_STATE")

for key in (
    "positive_mapping_authoring_precedes_successor_activation",
    "complete_roundtrip_machine_check_precedes_successor_activation",
    "independent_mapping_and_roundtrip_review_precedes_successor_activation",
):
    if v2["CV2_SR07_correction"][key] is not True:
        fail("GOVERNANCE_ORDER|" + key)

if review_record[
    "completed_review"
]["overall_decision"] != "REVISION_REQUIRED":
    fail("V1_REVIEW_OVERALL")

if evidence[
    "CVR05_corrected_outcome"
]["selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("EVIDENCE_OUTCOME")

if evidence[
    "CVR03_multifield_capability_boundary"
]["exhaustive_admissible_v2_capability_argument_available"] is not False:
    fail("EXHAUSTIVE_ARGUMENT_STATE")

if evidence[
    "CVR04_corrected_governance_order"
]["positive_mapping_precedes_successor_activation"] is not True:
    fail("MAPPING_ORDER")

if evidence[
    "CVR07_historical_pass_handling"
]["historical_pass_results_automatically_approve_corrective_v2"] is not False:
    fail("HISTORICAL_PASS_AUTO_APPROVAL")

packet = FILES["packet"].read_text(encoding="utf-8")

for i in range(1, 9):
    rid = f"CVR{i:02d}"

    if packet.count("### " + rid + " ") != 1:
        fail("REVIEW_ITEM_HEADING|" + rid)

decisions = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(decisions) != 8:
    fail("ITEM_DECISION_LINE_COUNT")

if any(x.strip() for x in decisions):
    fail("ITEM_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2 / "
    r"REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(overall) != 1:
    fail("OVERALL_DECISION_LINE_COUNT")

if overall[0].strip():
    fail("OVERALL_DECISION_NOT_BLANK")

for field in (
    "Reviewer role:",
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    lines = [
        line
        for line in packet.splitlines()
        if line.startswith(field)
    ]

    if len(lines) != 1:
        fail("REVIEWER_FIELD_COUNT|" + field)

    if lines[0][len(field):].strip():
        fail("REVIEWER_FIELD_NOT_BLANK|" + field)

manifest = json.loads(
    FILES["manifest"].read_text(encoding="utf-8")
)

if manifest[
    "human_review_state"
]["completed"] is not False:
    fail("HUMAN_REVIEW_ALREADY_COMPLETED")

if manifest[
    "human_review_state"
]["synthetic_decision"] is not False:
    fail("SYNTHETIC_DECISION")

for entry in manifest["package_files"]:
    path = HERE / entry["filename"]

    if not path.is_file():
        fail("MANIFEST_FILE_MISSING|" + entry["filename"])

    if sha(path) != entry["sha256"]:
        fail("MANIFEST_FILE_SHA|" + entry["filename"])

print("CORRECTIVE_V2_EXACT_BINDING=PASS")
print("CORRECTIVE_V2_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("NO_PROVEN_V2_MAPPING_DOES_NOT_EQUAL_NO_POSSIBLE_V2_MAPPING=YES")
print("EXHAUSTIVE_V2_MULTIFIELD_CAPABILITY_ARGUMENT_AVAILABLE=NO")
print("POSITIVE_MAPPING_AND_ROUNDTRIP_REVIEW_PRECEDE_ACTIVATION=YES")
print("HISTORICAL_V1_PASS_RESULTS_PRESERVED=YES")
print("CVR01_TO_CVR08_PRESENT=YES")
print("CVR01_TO_CVR08_INITIAL_DECISIONS_BLANK=YES")
print("OVERALL_CORRECTIVE_V2_REVIEW_DECISION_INITIAL_BLANK=YES")
print("REVIEWER_IDENTITY_FIELDS_INITIAL_BLANK=YES")
print("CORRECTIVE_V2_INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("SYNTHETIC_REVIEWER_DECISION=NO")
print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_CORRECTIVE_V2_REVIEW_PACKAGE_V1=PASS")
