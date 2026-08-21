#!/usr/bin/env python3

import collections
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "proof_json":
        HERE / "01_residual_schema_v2_insufficiency_proof.EXACT_COPY.v1.json",

    "proof_md":
        HERE / "02_residual_schema_v2_insufficiency_proof_summary.EXACT_COPY.v1.md",

    "v4":
        HERE / "03_curl_technical_protocol_working_draft_v4.EXACT_COPY.json",

    "v2":
        HERE / "04_active_protocol_specification_v2_schema.EXACT_COPY.json",

    "historical":
        HERE / "05_historical_curl_mapping_contract_v4.EXACT_COPY.json",

    "active_hash":
        HERE / "06_active_v2_hash_contract.EXACT_COPY.json",

    "dispatch":
        HERE / "07_active_version_dispatch.EXACT_COPY.json",

    "decision0068":
        HERE / "08_decision_0068_author_checkpoint.EXACT_COPY.md",

    "authorization0069":
        HERE / "09_decision_0069_review_package_authorization.EXACT_COPY.json",

    "evidence":
        HERE / "10_residual_insufficiency_review_evidence.v1.json",

    "packet":
        HERE / "11_residual_schema_v2_insufficiency_reviewer_packet.REVIEW_DRAFT.v1.md",

    "manifest":
        HERE / "13_residual_schema_v2_insufficiency_review_package_manifest.v1.json",
}

EXPECTED_SOURCE_SHA = {
    "proof_json":
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",

    "proof_md":
        "c9eddfbdfc29d3e3409dd4e674499e0712fdd604751e9fe01948cef9e5cff57b",

    "v4":
        "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8",

    "v2":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "historical":
        "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070",

    "active_hash":
        "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9",

    "dispatch":
        "67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee",

    "decision0068":
        "62b145c402716864533da8e067518b92176b88de07367cdd2296e546c3936863",

    "authorization0069":
        "0af2553566e8345fb3eb7ecf9b6c6afdf0818cc7e773643f7735f24080dff3eb",
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

for key, expected in EXPECTED_SOURCE_SHA.items():
    if sha(FILES[key]) != expected:
        fail(
            "EXACT_COPY_SHA|"
            + key
        )

proof = json.loads(
    FILES["proof_json"].read_text(
        encoding="utf-8"
    )
)

v4 = json.loads(
    FILES["v4"].read_text(
        encoding="utf-8"
    )
)

schema = json.loads(
    FILES["v2"].read_text(
        encoding="utf-8"
    )
)

historical = json.loads(
    FILES["historical"].read_text(
        encoding="utf-8"
    )
)

evidence = json.loads(
    FILES["evidence"].read_text(
        encoding="utf-8"
    )
)

manifest = json.loads(
    FILES["manifest"].read_text(
        encoding="utf-8"
    )
)

if proof["status"] != \
   "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_TECHNICAL_REVIEW":
    fail("PROOF_STATUS")

families = (
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
)

rules = [
    x
    for family in families
    for x in v4[family]
]

if len(rules) != 64:
    fail("RULE_COUNT")

if sum(
    "enforcement" in x
    for x in rules
) != 64:
    fail("ENFORCEMENT_COVERAGE")

values = {
    x["enforcement"]
    for x in rules
}

if len(values) != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

schema_raw = json.dumps(
    schema,
    sort_keys=True
).lower()

if "enforcement" in schema_raw:
    fail("V2_EXPLICIT_ENFORCEMENT_CARRIER")

by_verdict = collections.defaultdict(set)

for x in rules:
    by_verdict[
        x.get(
            "verdict",
            "<NO_EXPLICIT_VERDICT>"
        )
    ].add(
        x["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_verdict.values()
) != 3:
    fail("VERDICT_AMBIGUITY_COUNT")

by_dv = collections.defaultdict(set)

for x in rules:
    by_dv[
        (
            x.get(
                "defect",
                "<NO_DEFECT>"
            ),
            x.get(
                "verdict",
                "<NO_EXPLICIT_VERDICT>"
            ),
        )
    ].add(
        x["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_dv.values()
) != 4:
    fail("DEFECT_VERDICT_AMBIGUITY_COUNT")

expected_policy_gaps = {
    "normative_strength_uncertainty_must_not_be_silently_strengthened":
        "normative_strength",

    "resource_centered":
        "resource_centered",

    "synthetic_protocol_events_invented":
        "synthetic_protocol_events",
}

for field, token in expected_policy_gaps.items():
    if token in schema_raw:
        fail(
            "POLICY_GAP_NO_LONGER_PRESENT|"
            + field
        )

evidence_ri03 = evidence[
    "RI03_enforcement_evidence"
]

if evidence_ri03[
    "rule_record_count"
] != 64:
    fail("EVIDENCE_RULE_COUNT")

if evidence_ri03[
    "rules_with_enforcement"
] != 64:
    fail("EVIDENCE_ENFORCEMENT_COVERAGE")

if evidence_ri03[
    "distinct_enforcement_value_count"
] != 15:
    fail("EVIDENCE_ENFORCEMENT_VALUES")

if evidence_ri03[
    "verdict_to_enforcement_ambiguous_group_count"
] != 3:
    fail("EVIDENCE_VERDICT_AMBIGUITY")

if evidence_ri03[
    "defect_plus_verdict_to_enforcement_ambiguous_group_count"
] != 4:
    fail("EVIDENCE_DV_AMBIGUITY")

if evidence[
    "RI05_representation_policy_evidence"
]["unresolved_exact_field_count"] != 3:
    fail("EVIDENCE_POLICY_GAP_COUNT")

historical_ids = {
    x.get("obstruction_id")
    for x in historical.get(
        "structural_obstruction_witnesses",
        []
    )
    if isinstance(x, dict)
}

required_ids = {
    "V2-O1-MEMBERSHIP-RELATION",
    "V2-O2-FOUR-VERDICT-AND-JOIN-POLICY",
    "V2-O3-PATH-AND-SET-VALUED-REASONING",
    "V2-O4-STRUCTURED-RULE-PAYLOAD",
}

if not required_ids.issubset(
    historical_ids
):
    fail("HISTORICAL_OBSTRUCTION_SET")

resolved = evidence[
    "RI02_historical_resolved_obstructions"
]

if resolved["count"] != 4:
    fail("RESOLVED_OBSTRUCTION_COUNT")

for item in resolved["results"]:
    if item[
        "active_v2_direct_carrier_test"
    ] != "PASS":
        fail(
            "RESOLVED_CARRIER_TEST|"
            + item["obstruction_id"]
        )

packet = FILES["packet"].read_text(
    encoding="utf-8"
)

for i in range(1, 9):
    rid = f"RI{i:02d}"

    if packet.count(
        "### " + rid + " "
    ) != 1:
        fail(
            "REVIEW_ITEM_HEADING|"
            + rid
        )

item_decision_lines = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(item_decision_lines) != 8:
    fail("ITEM_DECISION_LINE_COUNT")

if any(
    x.strip()
    for x in item_decision_lines
):
    fail("ITEM_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision \(APPROVE_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(overall) != 1:
    fail("OVERALL_DECISION_LINE_COUNT")

if overall[0].strip():
    fail("OVERALL_DECISION_NOT_BLANK")

for field in (
    "Reviewer role:",
    "Reviewer name:",
    "Reviewer confirmation / initials:",
    "Review date:",
):
    matches = [
        line
        for line in packet.splitlines()
        if line.startswith(field)
    ]

    if len(matches) != 1:
        fail(
            "REVIEWER_FIELD_COUNT|"
            + field
        )

    if matches[0][len(field):].strip():
        fail(
            "REVIEWER_FIELD_NOT_BLANK|"
            + field
        )

if evidence[
    "human_review_state"
]["reviewer_decision_present"] is not False:
    fail("SYNTHETIC_REVIEW_DECISION")

if evidence[
    "human_review_state"
]["synthetic_reviewer_decision"] is not False:
    fail("SYNTHETIC_REVIEWER")

if manifest[
    "human_review_state"
]["completed"] is not False:
    fail("MANIFEST_HUMAN_REVIEW_STATE")

if manifest[
    "human_review_state"
]["synthetic_decision"] is not False:
    fail("MANIFEST_SYNTHETIC_DECISION")

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

print("PACKAGE_EXACT_SOURCE_BINDINGS=PASS")
print("RULE_RECORD_TOTAL=64")
print("RULES_WITH_ENFORCEMENT=64")
print("ENFORCEMENT_VALUE_COUNT=15")
print("V2_EXPLICIT_ENFORCEMENT_CARRIER_PRESENT=NO")
print("VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=3")
print("DEFECT_PLUS_VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=4")
print("UNRESOLVED_REPRESENTATION_POLICY_FIELD_COUNT=3")
print("HISTORICAL_RESOLVED_OBSTRUCTION_COUNT=4")
print("RI01_TO_RI08_PRESENT=YES")
print("RI01_TO_RI08_INITIAL_DECISIONS_BLANK=YES")
print("OVERALL_REVIEW_DECISION_INITIAL_BLANK=YES")
print("REVIEWER_IDENTITY_FIELDS_INITIAL_BLANK=YES")
print("SYNTHETIC_HUMAN_REVIEW_DECISION=NO")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_COMPLETED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_REVIEW_PACKAGE=PASS")
