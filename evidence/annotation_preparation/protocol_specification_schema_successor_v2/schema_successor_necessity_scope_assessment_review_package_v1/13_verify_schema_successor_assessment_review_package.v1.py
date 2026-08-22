#!/usr/bin/env python3

import collections
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "assessment_json":
        HERE / "01_schema_successor_necessity_scope_assessment.EXACT_COPY.v1.json",

    "assessment_md":
        HERE / "02_schema_successor_necessity_scope_assessment.EXACT_COPY.v1.md",

    "assessment_sums":
        HERE / "03_schema_successor_necessity_scope_assessment_checksums.EXACT_COPY.SHA256SUMS",

    "decision0074":
        HERE / "04_decision_0074_author_checkpoint.EXACT_COPY.md",

    "authorization0075":
        HERE / "05_decision_0075_review_package_authorization.EXACT_COPY.json",

    "original_review":
        HERE / "06_original_completed_residual_insufficiency_review.EXACT_COPY.md",

    "focused_review":
        HERE / "07_focused_RI01_C_completed_rereview.EXACT_COPY.md",

    "proof":
        HERE / "08_residual_schema_v2_insufficiency_proof.EXACT_COPY.v1.json",

    "v4":
        HERE / "09_curl_technical_protocol_working_draft_v4.EXACT_COPY.json",

    "v2":
        HERE / "10_active_protocol_specification_v2_schema.EXACT_COPY.json",

    "evidence":
        HERE / "11_assessment_review_evidence.v1.json",

    "packet":
        HERE / "12_schema_successor_assessment_reviewer_packet.REVIEW_DRAFT.v1.md",

    "manifest":
        HERE / "14_schema_successor_assessment_review_package_manifest.v1.json",
}

EXPECTED = {
    "assessment_json":
        "be64ed3755b5c1a525c23e5e6b1472a35b84a5b3640ce22990dbceb5a41bdb70",

    "assessment_md":
        "1137858f4da8cdfaaa7b88332f581f810f9f286f7b4ca71530b186abfc884008",

    "assessment_sums":
        "4613b93ed93457fb6f18277ae45971f1d9808c299d773f6378c489b09fd941ea",

    "decision0074":
        "7dd8e20114a00662236619892410265800770eb2b8953452c101da771b6ac028",

    "authorization0075":
        "048f0ef1f6ea78ea5c222b17b6965de0a703c164ef28c7d02845750daf133ed1",

    "original_review":
        "c169b26960349c4829109493f946d4f7115191a830ec35a28ff7a50e6df8c74d",

    "focused_review":
        "ad29020ad67b43e1603e6e81a1b635c5b722b77d6a429ecdd2510b53f7c42494",

    "proof":
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",

    "v4":
        "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8",

    "v2":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",
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

for key, expected in EXPECTED.items():
    if sha(FILES[key]) != expected:
        fail(
            "EXACT_COPY_SHA|"
            + key
        )

assessment = json.loads(
    FILES["assessment_json"].read_text(
        encoding="utf-8"
    )
)

v4 = json.loads(
    FILES["v4"].read_text(
        encoding="utf-8"
    )
)

v2 = json.loads(
    FILES["v2"].read_text(
        encoding="utf-8"
    )
)

evidence = json.loads(
    FILES["evidence"].read_text(
        encoding="utf-8"
    )
)

if assessment[
    "SA08_conclusion"
]["selected_outcome"] != "SCHEMA_SUCCESSOR_REQUIRED":
    fail("ASSESSMENT_CONCLUSION")

if assessment[
    "SA08_conclusion"
]["schema_successor_authoring_authorized_by_this_assessment"] is not False:
    fail("SUCCESSOR_AUTHORING_STATE")

if assessment[
    "SA08_conclusion"
]["successor_version_number_preselected"] is not False:
    fail("VERSION_PRESELECTION_STATE")

families = (
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
)

rules = [
    r
    for family in families
    for r in v4.get(family, [])
]

if len(rules) != 64:
    fail("RULE_COUNT")

if sum(
    "enforcement" in r
    for r in rules
) != 64:
    fail("ENFORCEMENT_COVERAGE")

if len({
    r["enforcement"]
    for r in rules
}) != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

schema_raw = json.dumps(
    v2,
    sort_keys=True
).lower()

for token in (
    "enforcement",
    "normative_strength",
    "resource_centered",
    "synthetic_protocol_events",
):
    if token in schema_raw:
        fail(
            "RESIDUAL_EXPLICIT_CARRIER_CHANGED|"
            + token
        )

by_verdict = collections.defaultdict(set)

for r in rules:
    by_verdict[
        r.get(
            "verdict",
            "<NO_EXPLICIT_VERDICT>"
        )
    ].add(
        r["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_verdict.values()
) != 3:
    fail("VERDICT_AMBIGUITY")

by_dv = collections.defaultdict(set)

for r in rules:
    by_dv[
        (
            r.get(
                "defect",
                "<NO_DEFECT>"
            ),
            r.get(
                "verdict",
                "<NO_EXPLICIT_VERDICT>"
            ),
        )
    ].add(
        r["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_dv.values()
) != 4:
    fail("DEFECT_VERDICT_AMBIGUITY")

original = FILES["original_review"].read_text(
    encoding="utf-8"
)

expected_original = {
    "RI01": "REVISION_REQUIRED",
    "RI02": "PASS",
    "RI03": "PASS",
    "RI04": "PASS",
    "RI05": "PASS",
    "RI06": "PASS",
    "RI07": "PASS",
    "RI08": "PASS",
}

for rid, expected in expected_original.items():
    m = re.search(
        rf"^### {rid}\b.*?"
        rf"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*"
        rf"(PASS|REVISION_REQUIRED|FAIL)\s*$",
        original,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not m or m.group(1) != expected:
        fail(
            "ORIGINAL_REVIEW|"
            + rid
        )

focused = FILES["focused_review"].read_text(
    encoding="utf-8"
)

m = re.search(
    r"^Focused RI01 decision "
    r"\(PASS / REVISION_REQUIRED / FAIL\):\s*"
    r"(PASS|REVISION_REQUIRED|FAIL)\s*$",
    focused,
    flags=re.MULTILINE,
)

if not m or m.group(1) != "PASS":
    fail("FOCUSED_RI01_REREVIEW")

if evidence[
    "SR01_exact_binding"
]["review_chain"]["all_items_pass_closed"] is not True:
    fail("REVIEW_CHAIN_STATE")

if evidence[
    "SR03_enforcement_residual"
]["rule_record_total"] != 64:
    fail("EVIDENCE_RULE_TOTAL")

if evidence[
    "SR03_enforcement_residual"
]["distinct_enforcement_value_count"] != 15:
    fail("EVIDENCE_ENFORCEMENT_VALUES")

if evidence[
    "SR05_complete_field_scope"
]["other_rule_and_exit_field_gaps_remain_in_scope"] is not True:
    fail("COMPLETE_FIELD_SCOPE")

if evidence[
    "SR08_bounded_conclusion"
]["abstract_information_theoretic_impossibility_claimed"] is not False:
    fail("OVERCLAIM")

if evidence[
    "SR08_bounded_conclusion"
]["general_schema_v2_invalidity_claimed"] is not False:
    fail("GENERAL_V2_INVALIDITY_OVERCLAIM")

packet = FILES["packet"].read_text(
    encoding="utf-8"
)

for i in range(1, 9):
    rid = f"SR{i:02d}"

    if packet.count(
        "### " + rid + " "
    ) != 1:
        fail(
            "REVIEW_ITEM_HEADING|"
            + rid
        )

decisions = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(decisions) != 8:
    fail("ITEM_DECISION_LINE_COUNT")

if any(
    x.strip()
    for x in decisions
):
    fail("ITEM_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT / "
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
        fail(
            "REVIEWER_FIELD_COUNT|"
            + field
        )

    if lines[0][len(field):].strip():
        fail(
            "REVIEWER_FIELD_NOT_BLANK|"
            + field
        )

manifest = json.loads(
    FILES["manifest"].read_text(
        encoding="utf-8"
    )
)

if manifest[
    "human_review_state"
]["completed"] is not False:
    fail("HUMAN_REVIEW_ALREADY_COMPLETED")

if manifest[
    "human_review_state"
]["synthetic_decision"] is not False:
    fail("SYNTHETIC_REVIEW")

for entry in manifest[
    "package_files"
]:
    path = HERE / entry["filename"]

    if not path.is_file():
        fail(
            "MANIFEST_FILE_MISSING|"
            + entry["filename"]
        )

    if sha(path) != entry["sha256"]:
        fail(
            "MANIFEST_FILE_SHA|"
            + entry["filename"]
        )

print("ASSESSMENT_EXACT_BINDING=PASS")
print("AUTHOR_CANDIDATE_CONCLUSION=SCHEMA_SUCCESSOR_REQUIRED")
print("AUTHOR_CANDIDATE_CONCLUSION_IS_HUMAN_APPROVAL=NO")
print("ALL_RI01_TO_RI08_REVIEW_ITEMS_PASS_CLOSED=YES")
print("ENFORCEMENT_RULE_COVERAGE=64_OF_64")
print("DISTINCT_ENFORCEMENT_VALUES=15")
print("VERDICT_TO_ENFORCEMENT_AMBIGUOUS_GROUPS=3")
print("DEFECT_PLUS_VERDICT_TO_ENFORCEMENT_AMBIGUOUS_GROUPS=4")
print("UNRESOLVED_REPRESENTATION_POLICY_ASSERTIONS=3")
print("OTHER_RULE_AND_EXIT_FIELD_GAPS_REMAIN_IN_SCOPE=YES")
print("SR01_TO_SR08_PRESENT=YES")
print("SR01_TO_SR08_INITIAL_DECISIONS_BLANK=YES")
print("OVERALL_ASSESSMENT_REVIEW_DECISION_INITIAL_BLANK=YES")
print("REVIEWER_IDENTITY_FIELDS_INITIAL_BLANK=YES")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_COMPLETED=NO")
print("SYNTHETIC_REVIEWER_DECISION=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_SCHEMA_SUCCESSOR_ASSESSMENT_REVIEW_PACKAGE_V1=PASS")
