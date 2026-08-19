#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


here = Path(__file__).resolve().parent

bindingp = here / "01_repository_binding.v1.json"
reviewp = here / "02_v2_schema_insufficiency_reviewer_packet.BLANK.v1.md"
v2p = here / "03_exact_v2_mapping_contract.v2.json"
checkpointp = here / "04_v2_schema_insufficiency_author_checkpoint.v1.json"
v4p = here / "06_exact_approved_curl_v4.json"
schemap = here / "07_frozen_canonical_schema.json"
authp = here / "08_v2_successor_authorization.v1.json"
v1p = here / "10_exact_v1_mapping_contract.v1.json"
v1reviewp = here / "11_completed_v1_human_review.md"
v1recordp = here / "12_completed_v1_human_review_record.v1.json"
manifestp = here / "14_review_package_manifest.v1.json"


V2_SHA = (
    "f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c"
)

V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

SCHEMA_SHA = (
    "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
)

AUTH_SHA = (
    "5d3771c4748731642f3068722e986e65479a9b85d1087737e2faeb2dc76b073b"
)

V1_SHA = (
    "31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257"
)

V1_REVIEW_SHA = (
    "a19d4a6132be417798b027794045227949ea40265e11714543e85ef1c325ad73"
)

V1_RECORD_SHA = (
    "b7a8572b3893d83e411c4d79a56682c9b3a47345ed25396df5dcc4556d8a161d"
)


if sha(v2p) != V2_SHA:
    fail("EXACT_V2_SHA")

if v2p.stat().st_size != 18515:
    fail("EXACT_V2_SIZE")

if sha(v4p) != V4_SHA:
    fail("EXACT_V4_SHA")

if v4p.stat().st_size != 41033:
    fail("EXACT_V4_SIZE")

if sha(schemap) != SCHEMA_SHA:
    fail("FROZEN_SCHEMA_SHA")

if sha(authp) != AUTH_SHA:
    fail("V2_AUTHORIZATION_SHA")

if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if sha(v1reviewp) != V1_REVIEW_SHA:
    fail("V1_HUMAN_REVIEW_SHA")

if sha(v1recordp) != V1_RECORD_SHA:
    fail("V1_HUMAN_REVIEW_RECORD_SHA")


binding = json.loads(
    bindingp.read_text(encoding="utf-8")
)

if binding["repository_binding"][
    "author_checkpoint_commit"
] != "9bc2d448cf2c08a728174090c3d819bbdb9e28f1":
    fail("AUTHOR_CHECKPOINT_COMMIT")

if binding["repository_binding"][
    "author_checkpoint_tree"
] != "9cb9b34bbeb45cc5916543a04e0f0dad8f54af50":
    fail("AUTHOR_CHECKPOINT_TREE")

if binding["exact_review_target"][
    "independently_approved"
] is not False:
    fail("SYNTHETIC_V2_APPROVAL")


v2 = json.loads(
    v2p.read_text(encoding="utf-8")
)

expected_outcome = (
    "FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_"
    "SCHEMA_SUCCESSOR_REQUIRED"
)

if v2["contract_kind"] != \
        "FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF":
    fail("V2_CONTRACT_KIND")

if v2["author_outcome"] != expected_outcome:
    fail("V2_AUTHOR_OUTCOME")

if v2["status"] != \
        "AUTHOR_CHECKPOINT_INDEPENDENT_REVIEW_REQUIRED":
    fail("V2_STATUS")

inventory = v2["frozen_inventory"]

expected_inventory = {
    "semantic_container_count": 10,
    "api_surface_function_count": 12,
    "resource_component_count": 5,
    "global_runtime_rule_count": 10,
    "easy_handle_rule_count": 21,
    "multi_handle_rule_count": 29,
    "cross_resource_rule_count": 4,
    "total_rule_record_count": 64,
    "exit_obligation_count": 3,
}

for key, expected in expected_inventory.items():
    if inventory[key] != expected:
        fail(
            "V2_INVENTORY|"
            + key
        )

if inventory["allowed_machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("FOUR_VERDICT_CONTRACT")


witnesses = {
    x["obstruction_id"]: x
    for x in v2[
        "structural_obstruction_witnesses"
    ]
}

if set(witnesses) != {
    "V2-O1-MEMBERSHIP-RELATION",
    "V2-O2-FOUR-VERDICT-AND-JOIN-POLICY",
    "V2-O3-PATH-AND-SET-VALUED-REASONING",
    "V2-O4-STRUCTURED-RULE-PAYLOAD",
}:
    fail("OBSTRUCTION_WITNESS_SET")


if witnesses[
    "V2-O4-STRUCTURED-RULE-PAYLOAD"
]["structured_value_occurrence_count"] != 12:
    fail("STRUCTURED_RULE_VALUE_COUNT")

if witnesses[
    "V2-O4-STRUCTURED-RULE-PAYLOAD"
]["frozen_schema_facts"][
    "canonical_obligation_object_typed_field_count"
] != 0:
    fail("CANONICAL_OBLIGATION_OBJECT_CARRIER_COUNT")


proof = v2["formal_insufficiency_argument"]

if proof[
    "frozen_schema_insufficiency_demonstrated_under_current_contract"
] is not True:
    fail("AUTHOR_INSUFFICIENCY_CONCLUSION")

if proof[
    "schema_successor_required"
] is not True:
    fail("AUTHOR_SCHEMA_SUCCESSOR_REQUIREMENT")

if proof[
    "schema_successor_authorized_by_this_contract"
] is not False:
    fail("SCHEMA_SUCCESSOR_PREMATURELY_AUTHORIZED")

if proof[
    "positive_mapping_candidate_authored"
] is not False:
    fail("POSITIVE_MAPPING_PREMATURELY_AUTHORED")


for key in (
    "positive_mapping_algorithm_defined",
    "positive_mapping_algorithm_approved",
    "lossless_v4_to_frozen_schema_mapping_proven",
    "canonical_materialization_safe",
    "curl_json_creation_authorized",
    "curl_json_created",
    "canonical_schema_successor_authorized",
):
    if v2[key] is not False:
        fail(
            "V2_PROHIBITED_POSITIVE_STATUS|"
            + key
        )


schema = json.loads(
    schemap.read_text(encoding="utf-8")
)

if schema.get("additionalProperties") is not False:
    fail("FROZEN_SCHEMA_NOT_CLOSED")


auth = json.loads(
    authp.read_text(encoding="utf-8")
)

boundary = auth["representation_design_boundary"]

for key in (
    "opaque_payload_packing_authorized",
    "semantic_protocol_event_invention_authorized",
    "protocol_rule_addition_authorized",
    "protocol_rule_removal_authorized",
    "protocol_rule_semantic_change_authorized",
    "machine_verdict_contract_change_authorized",
    "source_evidence_change_authorized",
):
    if boundary[key] is not False:
        fail(
            "AUTH_BOUNDARY|"
            + key
        )


text = reviewp.read_text(
    encoding="utf-8"
)

for i in range(1, 11):
    rr = f"V2-RR{i:02d}"

    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            text,
            re.M,
        )
    )

    if len(heads) != 1:
        fail(
            f"REVIEW_ITEM_HEADING|{rr}|{len(heads)}"
        )

    tail = text[heads[0].end():]

    nxt = re.search(
        r"^###\s+V2-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    decisions = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M,
    )

    if len(decisions) != 1:
        fail(
            f"REVIEW_DECISION_FIELD_COUNT|{rr}|{len(decisions)}"
        )

    if decisions[0].strip():
        fail(
            "REVIEW_DECISION_NOT_BLANK|"
            + rr
        )


overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    text,
    re.M,
)

if len(overall) != 1:
    fail("OVERALL_DECISION_FIELD_COUNT")

if overall[0].strip():
    fail("OVERALL_DECISION_NOT_BLANK")


for label in (
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    vals = re.findall(
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        text,
        re.M,
    )

    if len(vals) != 1:
        fail(
            "REVIEWER_IDENTITY_FIELD_COUNT|"
            + label
        )

    if vals[0].strip():
        fail(
            "REVIEWER_IDENTITY_NOT_BLANK|"
            + label
        )


if (
    "Reviewer role ID: `Spec-Technical-Reviewer-1`"
    not in text
):
    fail("REVIEWER_ROLE_ID")


manifest = json.loads(
    manifestp.read_text(encoding="utf-8")
)

if manifest["review_target_sha256"] != V2_SHA:
    fail("MANIFEST_REVIEW_TARGET_SHA")

if manifest["human_review_completed"] is not False:
    fail("MANIFEST_HUMAN_REVIEW_STATUS")

if manifest[
    "synthetic_human_approval_present"
] is not False:
    fail("MANIFEST_SYNTHETIC_APPROVAL")

if manifest[
    "schema_successor_authorized"
] is not False:
    fail("MANIFEST_SCHEMA_SUCCESSOR_STATUS")

if manifest[
    "curl_json_created"
] is not False:
    fail("MANIFEST_CURL_JSON_STATUS")


for rec in manifest["package_members"]:
    p = here / rec["path"]

    if not p.is_file():
        fail(
            "MANIFEST_MEMBER_MISSING|"
            + rec["path"]
        )

    if sha(p) != rec["sha256"]:
        fail(
            "MANIFEST_MEMBER_SHA|"
            + rec["path"]
        )

    if p.stat().st_size != rec["size_bytes"]:
        fail(
            "MANIFEST_MEMBER_SIZE|"
            + rec["path"]
        )


print("EXACT_V2_REVIEW_TARGET_SHA256=PASS")
print("EXACT_V2_REVIEW_TARGET_SIZE=PASS")
print("V2_AUTHOR_CHECKPOINT_BINDING=PASS")
print("APPROVED_V4_BINDING=PASS")
print("FROZEN_CANONICAL_SCHEMA_BINDING=PASS")
print("V2_SUCCESSOR_AUTHORIZATION_BINDING=PASS")
print("V1_MAPPING_CONTRACT_BINDING=PASS")
print("COMPLETED_V1_HUMAN_REVIEW_BINDING=PASS")
print("V2_CONTRACT_KIND=FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF")
print("V2_AUTHOR_OUTCOME=" + expected_outcome)
print("V2_AUTHOR_OUTCOME_INDEPENDENTLY_APPROVED=NO")
print("SEMANTIC_CONTAINER_COUNT=10")
print("API_SURFACE_FUNCTION_COUNT=12")
print("RESOURCE_COMPONENT_COUNT=5")
print("TOTAL_RULE_RECORD_COUNT=64")
print("EXIT_OBLIGATION_COUNT=3")
print("FOUR_VERDICT_CONTRACT=PASS")
print("STRUCTURAL_OBSTRUCTION_WITNESS_COUNT=4")
print("STRUCTURED_RULE_VALUE_OCCURRENCES=12")
print("CANONICAL_OBLIGATION_OBJECT_TYPED_CARRIERS=0")
print("OPAQUE_PAYLOAD_PACKING_AUTHORIZED=NO")
print("SEMANTIC_PROTOCOL_EVENT_INVENTION_AUTHORIZED=NO")
print("POSITIVE_MAPPING_APPROVED=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CANONICAL_MATERIALIZATION_SAFE=NO")
print("CURL_JSON_CREATED=NO")
print("V2_RR01_TO_V2_RR10_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("REVIEWER_ROLE_ID=Spec-Technical-Reviewer-1")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("CURL_V2_SCHEMA_INSUFFICIENCY_REVIEW_PACKAGE_VERIFICATION=PASS")
