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
    "02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json":
        "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9",

    "04_exact_source_reviewed_v2_hash_contract.json":
        "8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0",

    "05_exact_finalization_authorization.json":
        "87ac9317e19bad653c5a820685ba4102cd87a959a9acae037331109b6bd63e47",

    "07_exact_activation_governance_human_approval_record.json":
        "a118cfd294f5a00fd0f8e124e464c791eaf97229c643b44b981882294191ef18",

    "08_exact_approved_schema_v2.json":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "09_exact_frozen_v1_hash_contract.json":
        "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f",

    "10_exact_frozen_v1_schema.json":
        "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34",

    "11_exact_decision_0019.md":
        "50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9",

    "12_exact_frozen_zlib_v1.json":
        "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1",

    "13_exact_frozen_libpcap_v1.json":
        "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"
}

for rel, digest in expected.items():
    p = here / rel

    if not p.exists():
        fail("MISSING|" + rel)

    if sha(p) != digest:
        fail("SHA|" + rel)

if (
    here /
    "02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json"
).stat().st_size != 3154:
    fail("ACTIVE_FORM_SIZE")

subprocess.check_call(
    [
        "python3",
        str(
            here /
            "15_prepackage_repository_binding_proof/"
            "99_verify_prepackage_hash_finalization_binding.v1.py"
        )
    ]
)

binding = json.loads(
    (
        here /
        "01_finalization_binding.v1.json"
    ).read_text(encoding="utf-8")
)

if binding["status"] != \
   "READY_FOR_INDEPENDENT_HUMAN_REVIEW_NOT_INSTALLED":
    fail("PACKAGE_STATUS")

if binding["active_path_created"] is not False:
    fail("ACTIVE_PATH_CREATED")

if binding["schema_v2_activated"] is not False:
    fail("SCHEMA_ACTIVATED")

if binding["decision_0019_successor_adopted"] is not False:
    fail("SUCCESSOR_ADOPTED")

if binding["version_dispatch_activated"] is not False:
    fail("DISPATCH_ACTIVE")

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

src = json.loads(
    (
        here /
        "04_exact_source_reviewed_v2_hash_contract.json"
    ).read_text(encoding="utf-8")
)

dst = json.loads(
    (
        here /
        "02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json"
    ).read_text(encoding="utf-8")
)

diff = json.loads(
    (
        here /
        "03_exact_three_scalar_delta.v1.json"
    ).read_text(encoding="utf-8")
)

if src["status"] != "REVIEW_CANDIDATE_NOT_ACTIVE":
    fail("SOURCE_STATUS")

if dst["status"] != \
   "FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION":
    fail("TARGET_STATUS")

if dst["draft_boundary"][
    "review_candidate_is_not_active_contract"
] is not False:
    fail("TARGET_REVIEW_FLAG")

if dst["draft_boundary"][
    "active_path_must_not_be_created_until_later_reviewed_activation_decision"
] is not False:
    fail("TARGET_PATH_FLAG")

changes = []

def walk(a, b, path="$"):
    if type(a) is not type(b):
        changes.append((path, a, b))
        return

    if isinstance(a, dict):
        if set(a) != set(b):
            changes.append(
                (path + ".__keys__", sorted(a), sorted(b))
            )
            return

        for key in sorted(a):
            walk(
                a[key],
                b[key],
                path + "." + key
            )

    elif isinstance(a, list):
        if len(a) != len(b):
            changes.append(
                (path + ".__len__", len(a), len(b))
            )
            return

        for i, (x, y) in enumerate(zip(a, b)):
            walk(
                x,
                y,
                path + f"[{i}]"
            )

    elif a != b:
        changes.append((path, a, b))

walk(src, dst)

expected_paths = {
    "$.status",
    "$.draft_boundary.review_candidate_is_not_active_contract",
    "$.draft_boundary.active_path_must_not_be_created_until_later_reviewed_activation_decision"
}

if len(changes) != 3:
    fail("DELTA_COUNT")

if {x[0] for x in changes} != expected_paths:
    fail("DELTA_PATHS")

if diff["exact_delta_count"] != 3:
    fail("DIFF_COUNT")

if diff["all_other_values_identical"] is not True:
    fail("DIFF_IDENTITY")

pretty = (
    json.dumps(
        dst,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False
    )
    + "\n"
).encode("utf-8")

canonical = json.dumps(
    dst,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False
).encode("utf-8")

if hashlib.sha256(pretty).hexdigest() != \
   "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9":
    fail("TARGET_SERIALIZATION_SHA")

if len(pretty) != 3154:
    fail("TARGET_SERIALIZATION_SIZE")

if hashlib.sha256(canonical).hexdigest() != \
   "8f90f681c8942471ee05afc8d1fbb12d8208858163bc7f59695c26a82d48c4f6":
    fail("TARGET_CANONICAL_SHA")

preserve = (
    "contract_id",
    "schema_version",
    "reason",
    "dependencies",
    "canonical_json",
    "schema_content_sha256_carriers",
    "specification_content_sha256",
    "provenance_content_sha256",
    "computation_order",
    "prohibited_effects"
)

for key in preserve:
    if src[key] != dst[key]:
        fail("SEMANTIC_PRESERVATION|" + key)

for key in (
    "final_hashes_computed_only_after_required_review_fields_are_fixed",
    "schema_conformance_alone_does_not_imply_freeze"
):
    if src["draft_boundary"][key] != \
       dst["draft_boundary"][key]:
        fail("DRAFT_BOUNDARY_PRESERVATION|" + key)

matrix = json.loads(
    (
        here /
        "14_HF01_HF08_review_matrix.v1.json"
    ).read_text(encoding="utf-8")
)

if set(matrix) != {
    f"HF{i:02d}"
    for i in range(1, 9)
}:
    fail("HF_SET")

packet = (
    here /
    "16_hash_finalization_reviewer_packet.BLANK.v1.md"
).read_text(
    encoding="utf-8"
).replace(
    "\r\n",
    "\n"
).replace(
    "\r",
    "\n"
)

for i in range(1, 9):
    rid = f"HF{i:02d}"

    h = re.search(
        r"^##\s+"
        + re.escape(rid)
        + r"\b[^\n]*$",
        packet,
        re.M
    )

    if not h:
        fail("REVIEW_HEADING|" + rid)

    tail = packet[h.end():]

    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail("REVIEW_DECISION_NOT_BLANK|" + rid)

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
    "Human reviewer date"
):
    vals = re.findall(
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        packet,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail("IDENTITY_NOT_BLANK|" + label)

manifest = json.loads(
    (
        here /
        "18_schema_v2_hash_contract_finalization_package_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

if manifest["status"] != \
   "READY_FOR_INDEPENDENT_HUMAN_REVIEW_NOT_INSTALLED":
    fail("MANIFEST_STATUS")

if manifest["active_v2_hash_contract_created"] is not False:
    fail("MANIFEST_ACTIVE_HASH")

if manifest["schema_v2_activated"] is not False:
    fail("MANIFEST_SCHEMA_ACTIVATED")

if manifest["human_review_fields_initially_blank"] is not True:
    fail("MANIFEST_BLANK")

if manifest[
    "postcommit_package_noninterference_handoff_proof_required"
] is not True:
    fail("MANIFEST_POSTCOMMIT_PROOF")

for item in manifest["files"]:
    p = here / item["path"]

    if not p.exists():
        fail("MANIFEST_MISSING|" + item["path"])

    if sha(p) != item["sha256"]:
        fail("MANIFEST_SHA|" + item["path"])

    if p.stat().st_size != item["size_bytes"]:
        fail("MANIFEST_SIZE|" + item["path"])

print("HF01_TO_HF08_PRESENT=PASS")
print("SOURCE_REVIEWED_V2_HASH_CONTRACT_BINDING=PASS")
print("ACTIVE_FORM_EXACT_THREE_SCALAR_DELTA=PASS")
print("ACTIVE_FORM_TARGET_STATUS=FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION")
print("ACTIVE_FORM_FILE_SHA256=37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9")
print("ACTIVE_FORM_CANONICAL_JSON_SHA256=8f90f681c8942471ee05afc8d1fbb12d8208858163bc7f59695c26a82d48c4f6")
print("ALL_OTHER_HASH_CONTRACT_SEMANTICS_PRESERVED=YES")
print("HF01_TO_HF08_REVIEW_DECISIONS_INITIAL_STATE=BLANK")
print("HASH_FINALIZATION_OVERALL_DECISION_INITIAL_STATE=BLANK")
print("HASH_FINALIZATION_REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("SELF_CONTAINED_SCHEMA_V2_HASH_FINALIZATION_PACKAGE_VERIFICATION=PASS")
