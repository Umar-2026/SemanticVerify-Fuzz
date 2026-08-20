#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def csha(x):
    return hashlib.sha256(
        json.dumps(
            x,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()

here = Path(__file__).resolve().parent

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
DESIGN_SHA = "eb0367a18ca2474084a90b0aaf44b769b2ac2855f270b0d94814b35590749e90"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
AUTH_SHA = "96da6d7c3ea3da6e235182f93e2a228931ad7f5002648242f7bd786742bfd6f7"
V4_SHA = "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070"
V4_REVIEW_SHA = "6933bc89ab522e853640cc42f8ce3925e3fbc027a65ebc2f38bc083bf593649d"
V4_REVIEW_RECORD_SHA = "292a4a569139d4b09dc341579ab25bfdba0db60e44d7b42da36cf2ab0740e53d"
TECHV4_SHA = "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
PATHMAP_SHA = "4c6471d51627997f58b6c6bca833d364edc4c51e5aa7b80d0c34be8d63d19aaa"
HASH_SHA = "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f"
REP_SHA = "dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408"
LOSS_SHA = "c869079bfbd395b479e2dd8f2f1bcc31aabeababe0e24fc1542c6d35d210602e"

checks = {
    "03_exact_protocol_specification_schema_v2_candidate.json": V2_SHA,
    "04_schema_v2_successor_design_record.v1.json": DESIGN_SHA,
    "06_schema_v2_authoring_authorization.v1.json": AUTH_SHA,
    "08_frozen_protocol_specification_schema_v1.json": V1_SHA,
    "09_exact_approved_curl_mapping_contract_v4.json": V4_SHA,
    "10_completed_v4_human_review.APPROVED.md": V4_REVIEW_SHA,
    "11_completed_v4_human_review_record.v1.json": V4_REVIEW_RECORD_SHA,
    "13_exact_approved_curl_technical_v4.json": TECHV4_SHA,
    "15_canonical_protocol_specification_paths.v1.json": PATHMAP_SHA,
    "16_protocol_content_hash_canonicalization.v1.json": HASH_SHA,
}

for rel, expected in checks.items():
    p = here / rel
    if not p.exists():
        fail("MISSING|" + rel)
    if sha(p) != expected:
        fail("SHA|" + rel)

v2p = here / "03_exact_protocol_specification_schema_v2_candidate.json"

if v2p.stat().st_size != 43030:
    fail("V2_SIZE")

v2 = json.loads(v2p.read_text(encoding="utf-8"))
v1 = json.loads(
    (here / "08_frozen_protocol_specification_schema_v1.json")
    .read_text(encoding="utf-8")
)
v4 = json.loads(
    (here / "09_exact_approved_curl_mapping_contract_v4.json")
    .read_text(encoding="utf-8")
)
design = json.loads(
    (here / "04_schema_v2_successor_design_record.v1.json")
    .read_text(encoding="utf-8")
)

rep = v4["approved_v4_representation_policy_binding"]["exact_value"]
loss = v4["formal_insufficiency_argument"]["required_losslessness_contract"]

if len(rep) != 10 or csha(rep) != REP_SHA:
    fail("REPRESENTATION_POLICY_BINDING")

if len(loss) != 17 or csha(loss) != LOSS_SHA:
    fail("LOSSLESSNESS_BINDING")

basis = design["approved_v4_basis"]

if basis["representation_policy_path"] != \
   "$.approved_v4_representation_policy_binding.exact_value":
    fail("REP_PATH")

if basis["representation_policy_snapshot"] != rep:
    fail("REP_SNAPSHOT")

if basis["representation_policy_canonical_sha256"] != REP_SHA:
    fail("REP_DESIGN_SHA")

if basis["losslessness_contract_path"] != \
   "$.formal_insufficiency_argument.required_losslessness_contract":
    fail("LOSS_PATH")

if basis["losslessness_contract_snapshot"] != loss:
    fail("LOSS_SNAPSHOT")

if basis["losslessness_contract_canonical_sha256"] != LOSS_SHA:
    fail("LOSS_DESIGN_SHA")

if design["schema_v2_candidate"]["sha256"] != V2_SHA:
    fail("DESIGN_V2_SHA")

if design["schema_v2_candidate"]["size_bytes"] != 43030:
    fail("DESIGN_V2_SIZE")

Draft202012Validator.check_schema(v2)

if v2.get("additionalProperties") is not False:
    fail("TOP_LEVEL_OPEN")

def walk(x, path="$"):
    if isinstance(x, dict):
        yield path, x
        for k, v in x.items():
            yield from walk(v, path + "." + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, f"{path}[{i}]")

for path, obj in walk(v2):
    if obj.get("type") == "object" and \
       obj.get("additionalProperties") is not False:
        fail("OPEN_OBJECT|" + path)

for key in (
    "author",
    "content_sha256",
    "creation_date",
    "freeze_date",
    "library",
    "library_revision",
    "reviewer",
    "specification_id",
    "provenance",
):
    if v2["properties"][key] != v1["properties"][key]:
        fail("V1_METADATA_CARRIER|" + key)

event_kinds = set(
    v2["properties"]["events"]["items"]
    ["properties"]["event_kind"]["enum"]
)

if event_kinds != {
    "API_CALL",
    "BRANCH",
    "FUNCTION_EXIT"
}:
    fail("EVENT_KIND_BOUNDARY")

policy = v2["properties"]["semantic_policy"]["properties"]

if policy["verdict_vocabulary"]["const"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN"
]:
    fail("VERDICTS")

reason = policy["reasoning_model"]["properties"]

required_reason = {
    "path_sensitivity": "PATH_SENSITIVE",
    "state_domain": "SET_OF_FEASIBLE_STATES",
    "join_operator": "UNION_OF_FEASIBLE_STATES",
    "infeasible_path_handling": "EXCLUDE",
    "unknown_handling": "FIRST_CLASS_PRESERVE",
    "ownership_sensitivity": "RESOURCE_OWNERSHIP_SENSITIVE",
    "return_sensitivity": "RETURN_PREDICATE_SENSITIVE",
    "membership_sensitivity": "RELATION_MEMBERSHIP_SENSITIVE",
}

for k, v in required_reason.items():
    if reason[k].get("const") != v:
        fail("REASONING|" + k)

agg = policy["verdict_aggregation"]["properties"]

if agg["unknown_must_not_collapse_to_valid"].get("const") is not True:
    fail("UNKNOWN_TO_VALID")

rule = v2["properties"]["semantic_rules"]["items"]["properties"]

for k in (
    "resource_bindings",
    "relation_bindings",
    "preconditions",
    "effects",
    "verdict_if_violated",
    "source_evidence",
):
    if k not in rule:
        fail("RULE_CARRIER|" + k)

account = v2["properties"]["semantic_accounting"]["properties"]

for k in (
    "inventory",
    "forward_complete",
    "reverse_complete",
    "forward_accounting",
    "reverse_accounting",
):
    if k not in account:
        fail("ACCOUNTING|" + k)

binding = json.loads(
    (here / "01_repository_binding.v1.json")
    .read_text(encoding="utf-8")
)

for k in (
    "schema_v2_activated",
    "schema_v2_approved",
    "positive_v4_to_v2_mapping_defined",
    "curl_json_created",
    "synthetic_human_approval",
):
    if binding[k] is not False:
        fail("BINDING_NONAUTH|" + k)

packet = (
    (here / "02_schema_v2_reviewer_packet.BLANK.v1.md")
    .read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

for i in range(1, 11):
    rr = f"SV2-RR{i:02d}"
    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            packet,
            re.M
        )
    )

    if len(heads) != 1:
        fail("RR_HEADING|" + rr)

    tail = packet[heads[0].end():]

    nxt = re.search(
        r"^###\s+SV2-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M
    )

    sec = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        sec,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail("RR_NOT_BLANK|" + rr)

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
        "^" + re.escape(label) + r":[ \t]*(.*?)[ \t]*$",
        packet,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
        fail("IDENTITY_NOT_BLANK|" + label)

manifest = json.loads(
    (here / "19_review_package_manifest.v1.json")
    .read_text(encoding="utf-8")
)

if manifest["review_target"]["sha256"] != V2_SHA:
    fail("MANIFEST_V2")

if manifest["initial_human_decisions_blank"] is not True:
    fail("MANIFEST_BLANK")

if manifest["synthetic_human_approval"] is not False:
    fail("MANIFEST_SYNTHETIC")

if manifest["portability"][
    "package_verifier_requires_repository_git_directory"
] is not False:
    fail("MANIFEST_PORTABILITY")

for item in manifest["files"]:
    p = here / item["path"]

    if sha(p) != item["sha256"]:
        fail("MANIFEST_SHA|" + item["path"])

    if p.stat().st_size != item["size_bytes"]:
        fail("MANIFEST_SIZE|" + item["path"])

subprocess.check_call(
    [
        "python3",
        str(
            here /
            "22_git_object_proof/"
            "07_verify_git_object_proof.v1.py"
        ),
    ]
)

print("SCHEMA_V2_REVIEW_TARGET_EXACT_SHA256=PASS")
print("SCHEMA_V2_REVIEW_TARGET_EXACT_SIZE=PASS")
print("EXACT_V4_REPRESENTATION_POLICY_BINDING=PASS")
print("EXACT_V4_LOSSLESSNESS_BINDING=PASS")
print("SCHEMA_V2_JSON_SCHEMA_META_VALIDATION=PASS")
print("SCHEMA_V2_NORMATIVE_OBJECTS_CLOSED=PASS")
print("SCHEMA_V2_FOUR_VERDICT_POLICY=PASS")
print("SCHEMA_V2_PATH_SET_JOIN_POLICY=PASS")
print("SCHEMA_V2_STRUCTURED_RULE_CARRIERS=PASS")
print("SCHEMA_V2_FORWARD_REVERSE_ACCOUNTING=PASS")
print("SCHEMA_V2_REVIEW_ITEMS_10=PASS")
print("SCHEMA_V2_REVIEW_DECISIONS_INITIAL_STATE=BLANK")
print("SCHEMA_V2_REVIEW_OVERALL_INITIAL_STATE=BLANK")
print("SCHEMA_V2_REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("SYNTHETIC_HUMAN_APPROVAL=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_SCHEMA_V2_REVIEW_PACKAGE_VERIFICATION=PASS")
