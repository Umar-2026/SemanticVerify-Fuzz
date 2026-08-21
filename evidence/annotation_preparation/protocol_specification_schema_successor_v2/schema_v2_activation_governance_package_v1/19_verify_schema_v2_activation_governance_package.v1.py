#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

here = Path(__file__).resolve().parent

expected = {
    "03_exact_decision_0019.md":
        "50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9",

    "06_exact_v1_hash_contract.json":
        "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f",

    "10_exact_v1_schema.json":
        "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34",

    "11_exact_approved_v2_schema.json":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "12_exact_frozen_zlib_v1.json":
        "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1",

    "13_exact_frozen_libpcap_v1.json":
        "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73",

    "14_exact_canonical_path_map_v1.json":
        "4c6471d51627997f58b6c6bca833d364edc4c51e5aa7b80d0c34be8d63d19aaa",

    "15_exact_final_schema_v2_human_approval_record.json":
        "6a7c8c836071fe42522330f7b9ff75ec3cba3a855853756c3588c7a04844e1f8",

    "16_exact_activation_governance_authorization.json":
        "58778ad55c076ff3715ad218c6308514e274291d06e94fd95c4925ce5a9e963e",
}

for rel, digest in expected.items():
    p = here / rel

    if not p.exists():
        fail(
            "MISSING|" + rel
        )

    if sha(p) != digest:
        fail(
            "SHA|" + rel
        )

if (
    here /
    "11_exact_approved_v2_schema.json"
).stat().st_size != 43030:
    fail("V2_SCHEMA_SIZE")

subprocess.check_call(
    [
        "python3",
        str(
            here /
            "18_prepackage_repository_binding_proof/"
            "99_verify_prepackage_repository_binding.v1.py"
        )
    ]
)

binding = json.loads(
    (
        here /
        "01_activation_governance_binding.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if binding["status"] != \
   "REVIEW_CANDIDATE_NOT_ACTIVE":
    fail("PACKAGE_STATUS")

if binding["schema_v2"]["human_approved"] is not True:
    fail("V2_APPROVAL")

if binding["schema_v2"]["modified_by_package"] is not False:
    fail("V2_MODIFIED")

if binding["schema_v2"]["activated"] is not False:
    fail("V2_ACTIVATED")

if binding["decision_0019"]["modified_in_place"] is not False:
    fail("D0019_MODIFIED")

if binding["active_v2_hash_contract_created"] is not False:
    fail("ACTIVE_V2_HASH_CREATED")

if binding["positive_v4_to_v2_mapping_defined"] is not False:
    fail("POSITIVE_MAPPING")

if binding["curl_json_created"] is not False:
    fail("CURL_JSON")

if binding["human_review_required"] is not True:
    fail("HUMAN_REVIEW")

if binding[
    "postcommit_package_noninterference_handoff_proof_required"
] is not True:
    fail("POSTCOMMIT_PROOF_REQUIREMENT")

matrix = json.loads(
    (
        here /
        "02_AG01_AG09_requirements_matrix.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if set(matrix.keys()) != {
    f"AG{i:02d}"
    for i in range(1, 10)
}:
    fail("AG_SET")

v1 = json.loads(
    (
        here /
        "06_exact_v1_hash_contract.json"
    ).read_text(
        encoding="utf-8"
    )
)

v2schema = json.loads(
    (
        here /
        "11_exact_approved_v2_schema.json"
    ).read_text(
        encoding="utf-8"
    )
)

v2hash = json.loads(
    (
        here /
        "07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json"
    ).read_text(
        encoding="utf-8"
    )
)

if v2hash["contract_id"] != \
   "SVF-PROTOCOL-CONTENT-HASH-CANONICALIZATION-V2":
    fail("V2_HASH_ID")

if v2hash["schema_version"] != 2:
    fail("V2_HASH_VERSION")

if v2hash["status"] != \
   "REVIEW_CANDIDATE_NOT_ACTIVE":
    fail("V2_HASH_STATUS")

deps = v2hash["dependencies"]

if deps["protocol_specification_schema_path"] != \
   "config/schemas/protocol_specification.v2.schema.json":
    fail("V2_HASH_SCHEMA_PATH")

if deps["protocol_specification_schema_sha256"] != \
   "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956":
    fail("V2_HASH_SCHEMA_SHA")

if deps["schema_version_dispatch_value"] != "2.0.0":
    fail("V2_HASH_SCHEMA_VERSION_DISPATCH")

if v2hash["canonical_json"] != v1["canonical_json"]:
    fail("CANONICAL_JSON_RULE_CHANGE")

carriers = []

def walk(x, path="$"):
    if isinstance(x, dict):
        props = x.get("properties")

        if isinstance(props, dict) and \
           "content_sha256" in props:
            carriers.append(
                path +
                ".properties.content_sha256"
            )

        for k, v in x.items():
            walk(
                v,
                path + "." + str(k)
            )

    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(
                v,
                path + f"[{i}]"
            )

walk(v2schema)

carriers = sorted(set(carriers))

if carriers != \
   v2hash["schema_content_sha256_carriers"]:
    fail("V2_HASH_CARRIER_ACCOUNTING")

if "$.properties.content_sha256" not in carriers:
    fail("TOPLEVEL_HASH_CARRIER")

unsupported = [
    p for p in carriers
    if p != "$.properties.content_sha256"
    and "provenance" not in p.lower()
]

if unsupported:
    fail(
        "UNSUPPORTED_HASH_CARRIER|"
        + "|".join(unsupported)
    )

if v2hash[
    "specification_content_sha256"
][
    "schema_carrier"
] != "$.properties.content_sha256":
    fail("TOPLEVEL_HASH_RULE_BINDING")

dispatch = json.loads(
    (
        here /
        "09_version_dispatch_policy.REVIEW_CANDIDATE.json"
    ).read_text(
        encoding="utf-8"
    )
)

if dispatch["status"] != \
   "REVIEW_CANDIDATE_NOT_ACTIVE":
    fail("DISPATCH_STATUS")

if set(
    dispatch["dispatch"].keys()
) != {
    "1.0.0",
    "2.0.0"
}:
    fail("DISPATCH_SET")

if dispatch[
    "unsupported_or_missing_schema_version"
] != "REJECT":
    fail("UNKNOWN_VERSION_POLICY")

if dispatch[
    "heuristic_fallback_between_schema_versions"
] is not False:
    fail("HEURISTIC_FALLBACK")

if dispatch[
    "migration_of_existing_v1_artifacts"
] is not False:
    fail("V1_MIGRATION")

successor = (
    here /
    "05_proposed_decision_0019_successor.REVIEW_CANDIDATE.md"
).read_text(
    encoding="utf-8"
)

required_successor = (
    "Status: REVIEW CANDIDATE — NOT ACTIVE",
    "schema_version` is exactly `1.0.0",
    "schema_version` is exactly `2.0.0",
    "No heuristic fallback between schema versions is permitted.",
    "They are not rewritten, migrated, normalized, or rehashed",
    "It does not prove a lossless semantic mapping",
)

for term in required_successor:
    if term not in successor:
        fail(
            "SUCCESSOR_TERM|" + term
        )

packet = (
    here /
    "17_activation_governance_reviewer_packet.BLANK.v1.md"
).read_text(
    encoding="utf-8"
).replace(
    "\r\n",
    "\n"
).replace(
    "\r",
    "\n"
)

for i in range(1, 10):
    rid = f"AG{i:02d}"

    h = re.search(
        r"^##\s+"
        + re.escape(rid)
        + r"\b[^\n]*$",
        packet,
        re.M
    )

    if not h:
        fail(
            "REVIEW_HEADING|" + rid
        )

    tail = packet[h.end():]

    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = tail[
        :nxt.start()
    ] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail(
            "REVIEW_DECISION_NOT_BLANK|" + rid
        )

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    packet,
    re.M
)

if len(overall) != 1 or overall[0].strip():
    fail("OVERALL_NOT_BLANK")

for label in (
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    vals = re.findall(
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        packet,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail(
            "IDENTITY_NOT_BLANK|" + label
        )

manifest = json.loads(
    (
        here /
        "20_schema_v2_activation_governance_package_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if manifest["status"] != \
   "READY_FOR_INDEPENDENT_HUMAN_REVIEW_NOT_ACTIVE":
    fail("MANIFEST_STATUS")

if manifest["schema_v2_activated"] is not False:
    fail("MANIFEST_ACTIVATION")

if manifest[
    "active_v2_hash_contract_created"
] is not False:
    fail("MANIFEST_ACTIVE_HASH")

if manifest[
    "human_review_fields_initially_blank"
] is not True:
    fail("MANIFEST_HUMAN_STATE")

if manifest[
    "postcommit_package_noninterference_handoff_proof_required"
] is not True:
    fail("MANIFEST_POSTCOMMIT_PROOF")

for item in manifest["files"]:
    p = here / item["path"]

    if not p.exists():
        fail(
            "MANIFEST_MISSING|" + item["path"]
        )

    if sha(p) != item["sha256"]:
        fail(
            "MANIFEST_SHA|" + item["path"]
        )

    if p.stat().st_size != item["size_bytes"]:
        fail(
            "MANIFEST_SIZE|" + item["path"]
        )

print("ACTIVATION_GOVERNANCE_AG01_TO_AG09_PRESENT=PASS")
print("DECISION_0019_SUCCESSOR_REVIEW_CANDIDATE=PASS")
print("V2_HASH_CONTRACT_REVIEW_CANDIDATE=PASS")
print("V1_V2_VERSION_DISPATCH_REVIEW_CANDIDATE=PASS")
print("FROZEN_V1_NONMIGRATION_POLICY=PASS")
print("POSITIVE_V4_TO_V2_MAPPING_SEPARATION=PASS")
print("CURL_JSON_CREATION_AUTHORIZED=NO")
print("ANALYZER_BASELINE_REPAIR_AUTHORIZED=NO")
print("ACTIVATION_GOVERNANCE_REVIEW_DECISIONS_INITIAL_STATE=BLANK")
print("ACTIVATION_GOVERNANCE_OVERALL_DECISION_INITIAL_STATE=BLANK")
print("ACTIVATION_GOVERNANCE_REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("SCHEMA_V2_ACTIVATED=NO")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("SELF_CONTAINED_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE_VERIFICATION=PASS")
