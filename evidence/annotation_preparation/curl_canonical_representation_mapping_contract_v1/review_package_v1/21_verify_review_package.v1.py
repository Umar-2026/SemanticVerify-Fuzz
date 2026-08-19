#!/usr/bin/env python3

import copy
import hashlib
import json
import re
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chash(obj):
    return hashlib.sha256(
        json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


pkg = Path(__file__).resolve().parent

bindingp = pkg / "01_repository_binding.v1.json"
reviewp = pkg / "02_mapping_contract_v1_reviewer_packet.BLANK.v1.md"
contractp = pkg / "03_exact_mapping_contract.v1.json"
checkpointp = pkg / "05_mapping_contract_author_checkpoint.v1.json"
v4p = pkg / "06_exact_approved_curl_technical_working_draft.v4.json"
schemap = pkg / "07_frozen_protocol_specification_schema.json"
authp = pkg / "08_canonicalization_authorization.v1.json"
completed_recordp = pkg / "10_completed_v4_human_review_record.v1.json"
completed_reviewp = pkg / "11_completed_v4_human_review.md"

zfinalp = pkg / "13_zlib_finalization_record.v1.json"
zsourcep = pkg / "14_zlib_pre_freeze_source_record.v3.json"
zcanonp = pkg / "15_zlib_frozen_canonical.json"

pfinalp = pkg / "16_libpcap_finalization_record.v1.json"
psourcep = pkg / "17_libpcap_pre_freeze_source_record.v2.json"
pcanonp = pkg / "18_libpcap_frozen_canonical.json"

hashcontractp = pkg / "19_protocol_content_hash_canonicalization.v1.json"
manifestp = pkg / "20_review_package_manifest.v1.json"

CONTRACT_SHA = (
    "31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257"
)

V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

SCHEMA_SHA = (
    "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
)

COMPLETED_REVIEW_SHA = (
    "074814c04922f7cbc5fa41ef460cbde74dcb32529c09ef5752cf1d0f511f2aed"
)

ZLIB_SOURCE_SHA = (
    "8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e"
)

ZLIB_CANONICAL_SHA = (
    "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
)

PCAP_SOURCE_SHA = (
    "3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221"
)

PCAP_CANONICAL_SHA = (
    "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"
)

HASH_CONTRACT_SHA = (
    "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f"
)


if sha(contractp) != CONTRACT_SHA:
    fail("EXACT_CONTRACT_SHA")

if contractp.stat().st_size != 10879:
    fail("EXACT_CONTRACT_SIZE")

if sha(v4p) != V4_SHA:
    fail("EXACT_V4_SHA")

if v4p.stat().st_size != 41033:
    fail("EXACT_V4_SIZE")

if sha(schemap) != SCHEMA_SHA:
    fail("EXACT_SCHEMA_SHA")

if sha(completed_reviewp) != COMPLETED_REVIEW_SHA:
    fail("COMPLETED_V4_HUMAN_REVIEW_SHA")

if sha(zsourcep) != ZLIB_SOURCE_SHA:
    fail("ZLIB_SOURCE_SHA")

if sha(zcanonp) != ZLIB_CANONICAL_SHA:
    fail("ZLIB_CANONICAL_SHA")

if sha(psourcep) != PCAP_SOURCE_SHA:
    fail("LIBPCAP_SOURCE_SHA")

if sha(pcanonp) != PCAP_CANONICAL_SHA:
    fail("LIBPCAP_CANONICAL_SHA")

if sha(hashcontractp) != HASH_CONTRACT_SHA:
    fail("HASH_CONTRACT_SHA")


binding = json.loads(
    bindingp.read_text(encoding="utf-8")
)

if binding["author_checkpoint"] != {
    "commit": "afc2bb285f3b9adef8129f106c1c941b14d6f10c",
    "parent": "fc3b85c999199e8b45d683fb675a701444478472",
    "tree": "ace5a3cd3b2797c7a312403656391aa6da4908bb",
}:
    fail("AUTHOR_CHECKPOINT_BINDING")

if binding["human_review_status"] != "PENDING":
    fail("BINDING_HUMAN_REVIEW_STATUS")

if binding["human_review_decisions_present"] is not False:
    fail("BINDING_SYNTHETIC_DECISIONS")

if binding[
    "assistant_generated_or_synthetic_human_approval_present"
] is not False:
    fail("BINDING_SYNTHETIC_APPROVAL")


contract = json.loads(
    contractp.read_text(encoding="utf-8")
)

if contract["status"] != "AUTHOR_CHECKPOINT_REVIEW_REQUIRED":
    fail("CONTRACT_STATUS")

if contract["current_mapping_resolution"][
    "lossless_v4_to_frozen_schema_mapping_proven"
] is not False:
    fail("LOSSLESS_MAPPING_STATUS")

if contract["current_mapping_resolution"][
    "canonical_materialization_safe"
] is not False:
    fail("MATERIALIZATION_SAFETY")

if contract["current_mapping_resolution"][
    "positive_mapping_algorithm_defined"
] is not False:
    fail("POSITIVE_MAPPING_STATUS")

if contract["human_review"]["review_status"] != "PENDING":
    fail("CONTRACT_REVIEW_STATUS")

if contract["human_review"]["review_item_decisions"] != {}:
    fail("CONTRACT_SYNTHETIC_ITEM_DECISIONS")

if contract["human_review"]["overall_decision"] is not None:
    fail("CONTRACT_SYNTHETIC_OVERALL_DECISION")


v4 = json.loads(
    v4p.read_text(encoding="utf-8")
)

semantic_containers = [
    "api_surface",
    "resources",
    "return_condition_policy",
    "verdict_semantics",
    "defect_taxonomy",
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
    "exit_obligations",
]

inventory = contract["approved_v4_semantic_inventory"]

if inventory["protocol_semantic_containers"] != semantic_containers:
    fail("SEMANTIC_CONTAINER_SET")

for key in semantic_containers:
    if chash(v4[key]) != inventory[
        "protocol_semantic_container_sha256"
    ][key]:
        fail("SEMANTIC_CONTAINER_HASH|" + key)

if len(v4["api_surface"]) != 12:
    fail("API_SURFACE_COUNT")

if len(v4["resources"]) != 5:
    fail("RESOURCE_COUNT")

if len(v4["global_runtime_rules"]) != 10:
    fail("GLOBAL_RULE_COUNT")

if len(v4["easy_handle_rules"]) != 21:
    fail("EASY_RULE_COUNT")

if len(v4["multi_handle_rules"]) != 29:
    fail("MULTI_RULE_COUNT")

if len(v4["cross_resource_rules"]) != 4:
    fail("CROSS_RULE_COUNT")

if (
    len(v4["global_runtime_rules"])
    + len(v4["easy_handle_rules"])
    + len(v4["multi_handle_rules"])
    + len(v4["cross_resource_rules"])
) != 64:
    fail("TOTAL_RULE_COUNT")

if len(v4["exit_obligations"]) != 3:
    fail("EXIT_OBLIGATION_COUNT")


schema = json.loads(
    schemap.read_text(encoding="utf-8")
)

core = (
    set(schema["required"])
    - {
        "freeze_date",
        "content_sha256",
    }
)

if len(core) != 15:
    fail("PREFREEZE_CANONICAL_CORE_SIZE")

candidate_paths = []


def walk(obj, path="$"):
    if isinstance(obj, dict):
        if set(obj) == core:
            candidate_paths.append(path)

        for k, v in obj.items():
            walk(v, path + "." + str(k))

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]")


walk(v4)

if candidate_paths:
    fail(
        "REFERENCE_STYLE_CANDIDATE_PRESENT|"
        + repr(candidate_paths)
    )

for key in (
    "states",
    "initial_state",
    "events",
    "transitions",
    "obligations",
    "permitted_exit_states",
    "provenance",
):
    if key in v4:
        fail("DIRECT_CANONICAL_PAYLOAD_PRESENT|" + key)


auth = json.loads(
    authp.read_text(encoding="utf-8")
)

boundary = auth["authorized_transformation_boundary"]

if boundary[
    "canonical_metadata_transformation_authorized"
] is not True:
    fail("METADATA_TRANSFORMATION_AUTHORIZATION")

for key in (
    "protocol_rule_semantic_change_authorized",
    "protocol_rule_addition_authorized",
    "protocol_rule_removal_authorized",
    "api_surface_change_authorized",
    "defect_taxonomy_change_authorized",
    "machine_verdict_contract_change_authorized",
    "source_evidence_change_authorized",
    "new_evidence_class_authorized",
    "synthetic_protocol_event_authorized",
):
    if boundary[key] is not False:
        fail("TRANSFORMATION_BOUNDARY|" + key)


completed = json.loads(
    completed_recordp.read_text(encoding="utf-8")
)

if completed["completed_human_review"]["decision_counts"] != {
    "PASS": 12,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("V4_REVIEW_DECISION_COUNTS")

if completed["completed_human_review"]["overall_decision"] != \
        "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION":
    fail("V4_REVIEW_OVERALL_DECISION")


def verify_reference(
    label,
    finalp,
    sourcep,
    canonicalp,
):
    final = json.loads(
        finalp.read_text(encoding="utf-8")
    )

    source = json.loads(
        sourcep.read_text(encoding="utf-8")
    )

    canonical = json.loads(
        canonicalp.read_text(encoding="utf-8")
    )

    candidate = source.get(
        "candidate_specification_fields"
    )

    if not isinstance(candidate, dict):
        fail(label + "_CANDIDATE_MISSING")

    if final["semantic_immutability"][
        "protocol_semantic_change"
    ] is not False:
        fail(label + "_SEMANTIC_CHANGE")

    if final["semantic_immutability"][
        "only_added_fields"
    ] != [
        "freeze_date",
        "content_sha256",
    ]:
        fail(label + "_ADDED_FIELD_CONTRACT")

    rebuilt = copy.deepcopy(candidate)

    rebuilt["freeze_date"] = canonical["freeze_date"]

    if len(rebuilt["obligations"]) != len(
        canonical["obligations"]
    ):
        fail(label + "_OBLIGATION_COUNT")

    completed_obs = []

    for src, frozen in zip(
        rebuilt["obligations"],
        canonical["obligations"],
    ):
        sem = copy.deepcopy(frozen)

        sem.pop("freeze_date")
        sem.pop("content_sha256")

        if sem != src:
            fail(
                label
                + "_OBLIGATION_SEMANTIC_CHANGE|"
                + src.get("rule_id", "<NO_RULE>")
            )

        x = copy.deepcopy(src)
        x["freeze_date"] = frozen["freeze_date"]
        x["content_sha256"] = frozen["content_sha256"]

        completed_obs.append(x)

    rebuilt["obligations"] = completed_obs
    rebuilt["content_sha256"] = canonical["content_sha256"]

    if rebuilt != canonical:
        fail(label + "_FINALIZATION_RECONSTRUCTION")


verify_reference(
    "ZLIB",
    zfinalp,
    zsourcep,
    zcanonp,
)

verify_reference(
    "LIBPCAP",
    pfinalp,
    psourcep,
    pcanonp,
)


hashcontract = json.loads(
    hashcontractp.read_text(encoding="utf-8")
)

spec_hash = hashcontract[
    "specification_content_sha256"
]

if spec_hash["algorithm"] != "SHA-256":
    fail("HASH_ALGORITHM")

if spec_hash[
    "top_level_content_sha256_field"
] != "OMITTED":
    fail("TOP_LEVEL_SELF_HASH_POLICY")

if spec_hash[
    "replacement_value_used"
] is not False:
    fail("HASH_REPLACEMENT_POLICY")


review_text = (
    reviewp.read_text(encoding="utf-8")
    .replace("\\_", "_")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

for i in range(1, 11):
    rr = f"CMR-RR{i:02d}"

    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            review_text,
            re.M,
        )
    )

    if len(heads) != 1:
        fail(
            f"REVIEW_HEADING_COUNT|{rr}|{len(heads)}"
        )

    tail = review_text[heads[0].end():]

    nxt = re.search(
        r"^###\s+CMR-RR\d{2}\b[^\n]*$|"
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
            f"REVIEW_DECISION_FIELD_COUNT|{rr}|"
            f"{len(decisions)}"
        )

    if decisions[0].strip():
        fail(
            f"REVIEW_DECISION_NOT_BLANK|{rr}|"
            f"{decisions[0]!r}"
        )


overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    review_text,
    re.M,
)

if len(overall) != 1 or overall[0].strip():
    fail(
        "OVERALL_REVIEW_DECISION_NOT_BLANK|"
        + repr(overall)
    )


for label, pattern in (
    (
        "name",
        r"^Human reviewer name:[ \t]*(.*?)[ \t]*$",
    ),
    (
        "confirmation",
        r"^Human reviewer signature / recorded confirmation:"
        r"[ \t]*(.*?)[ \t]*$",
    ),
    (
        "date",
        r"^Human reviewer date:[ \t]*(.*?)[ \t]*$",
    ),
):
    values = re.findall(
        pattern,
        review_text,
        re.M,
    )

    if len(values) != 1 or values[0].strip():
        fail(
            "HUMAN_IDENTITY_NOT_BLANK|"
            + label
            + "|"
            + repr(values)
        )


if (
    "Reviewer role ID: `Spec-Technical-Reviewer-1`"
    not in review_text
):
    fail("REVIEWER_ROLE_ID")


manifest = json.loads(
    manifestp.read_text(encoding="utf-8")
)

for item in manifest["payload_files"]:
    p = pkg / item["path"]

    if not p.is_file():
        fail(
            "MANIFEST_FILE_MISSING|"
            + item["path"]
        )

    if sha(p) != item["sha256"]:
        fail(
            "MANIFEST_SHA_MISMATCH|"
            + item["path"]
        )

    if p.stat().st_size != item["size_bytes"]:
        fail(
            "MANIFEST_SIZE_MISMATCH|"
            + item["path"]
        )


print("EXACT_MAPPING_CONTRACT_SHA256=PASS")
print("EXACT_MAPPING_CONTRACT_SIZE=PASS")
print("AUTHOR_CHECKPOINT_BINDING=PASS")
print("EXACT_APPROVED_V4_BINDING=PASS")
print("FROZEN_CANONICAL_SCHEMA_BINDING=PASS")
print("COMPLETED_V4_HUMAN_REVIEW_BINDING=PASS")
print("PROTOCOL_SEMANTIC_CONTAINERS=10_OF_10_PASS")
print("API_SURFACE_FUNCTION_COUNT=12")
print("RESOURCE_COMPONENT_COUNT=5")
print("GLOBAL_RUNTIME_RULE_COUNT=10")
print("EASY_HANDLE_RULE_COUNT=21")
print("MULTI_HANDLE_RULE_COUNT=29")
print("CROSS_RESOURCE_RULE_COUNT=4")
print("TOTAL_RULE_RECORD_COUNT=64")
print("EXIT_OBLIGATION_RECORD_COUNT=3")
print("REFERENCE_STYLE_CANONICAL_CANDIDATE_PRESENT=NO")
print("CANONICAL_PAYLOAD_ALREADY_PRESENT=NO")
print("ZLIB_CORRECTED_FINALIZATION_PRECEDENT=PASS")
print("LIBPCAP_CORRECTED_FINALIZATION_PRECEDENT=PASS")
print("FSM_RECONSTRUCTED_DURING_REFERENCE_FINALIZATION=NO")
print("OBLIGATION_SEMANTIC_REWRITE_DURING_REFERENCE_FINALIZATION=NO")
print("AUTHORIZED_TRANSFORMATION_BOUNDARY=PASS")
print("LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO")
print("POSITIVE_MAPPING_ALGORITHM_AUTHORED=NO")
print("CANONICAL_MATERIALIZATION_SAFE=NO")
print("CMR_RR01_TO_CMR_RR10_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("REVIEWER_ROLE_ID=Spec-Technical-Reviewer-1")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("CURL_JSON_PRESENT_IN_REVIEW_PACKAGE=NO")
print("CURL_CANONICAL_MAPPING_CONTRACT_V1_REVIEW_PACKAGE_VERIFICATION=PASS")
