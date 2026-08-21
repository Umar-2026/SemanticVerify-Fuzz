#!/usr/bin/env python3

import copy
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

def git_blob_sha1(data):
    header = (
        "blob "
        + str(len(data))
        + "\0"
    ).encode("ascii")

    return hashlib.sha1(
        header + data
    ).hexdigest()

here = Path(__file__).resolve().parent

files = {
    "dispatch_target":
        here / "02_active_form_version_dispatch.REVIEW_CANDIDATE.json",

    "dispatch_diff":
        here / "03_exact_dispatch_delta.v1.json",

    "dispatch_source":
        here / "04_source_version_dispatch.REVIEWED_COPY.json",

    "successor_target":
        here / "05_active_form_decision_0019_successor.REVIEW_CANDIDATE.md",

    "successor_diff":
        here / "06_exact_successor_transformations.v1.json",

    "successor_source":
        here / "07_source_decision_0019_successor.REVIEWED_COPY.md",

    "hash_form":
        here / "08_approved_v2_hash_contract_active_form.EXACT_COPY.json",

    "hash_approval":
        here / "09_hash_contract_human_approval_record.EXACT_COPY.json",

    "authorization":
        here / "10_decision_0061_authorization.EXACT_COPY.json",

    "schema_v2":
        here / "12_schema_v2.EXACT_COPY.json",

    "v1_hash":
        here / "13_v1_hash_contract.EXACT_COPY.json",

    "decision_0019":
        here / "14_decision_0019.EXACT_COPY.md",

    "zlib":
        here / "15_zlib.EXACT_COPY.json",

    "libpcap":
        here / "16_libpcap.EXACT_COPY.json",

    "binding":
        here / "17_prepackage_repository_binding.v1.json",

    "matrix":
        here / "18_AF01_AF10_review_matrix.v1.md",

    "review":
        here / "19_activation_artifact_finalization_reviewer_packet.REVIEW_DRAFT.v1.md",

    "manifest":
        here / "21_schema_v2_activation_artifact_finalization_package_manifest.v1.json",

    "sums":
        here / "22_schema_v2_activation_artifact_finalization_package.v1.SHA256SUMS",
}

expected_sha = {
    "dispatch_source":
        "5a91a9938af7029edff6b91b8b624b2f0712680d49fad3abd1be29e649944bce",

    "dispatch_target":
        "67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee",

    "successor_source":
        "8665163eb5d4f7a8718ba3ed2d3973ba928fea85789c23696599a2d6ea02bbb3",

    "successor_target":
        "a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb",

    "hash_form":
        "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9",

    "hash_approval":
        "ef3badda87817a6245b767ed38a8a6e6498b23d88ce98bc2267693b1b377ae8a",

    "authorization":
        "7751d101532a9abb1bd896d10601e0cda29352255d3bce5c1491c62a9d8d199a",

    "schema_v2":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "v1_hash":
        "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f",

    "decision_0019":
        "50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9",

    "zlib":
        "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1",

    "libpcap":
        "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73",
}

for key, value in expected_sha.items():
    if sha(files[key]) != value:
        fail("SHA|" + key)

if files["successor_source"].stat().st_size != 2158:
    fail("SUCCESSOR_SOURCE_SIZE")

if files["successor_target"].stat().st_size != 2203:
    fail("SUCCESSOR_TARGET_SIZE")

if files["dispatch_target"].stat().st_size != 1334:
    fail("DISPATCH_TARGET_SIZE")

if files["hash_form"].stat().st_size != 3154:
    fail("HASH_FORM_SIZE")

if files["hash_approval"].stat().st_size != 3810:
    fail("HASH_APPROVAL_SIZE")

# Reconstruct exact dispatch target.
src = json.loads(
    files["dispatch_source"].read_text(
        encoding="utf-8"
    )
)

dst = copy.deepcopy(src)

if dst.get("status") != \
   "REVIEW_CANDIDATE_NOT_ACTIVE":
    fail("DISPATCH_SOURCE_STATUS")

dst["status"] = \
    "ACTIVE_UPON_EXPLICIT_SCHEMA_V2_ACTIVATION_DECISION"

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
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False
).encode("utf-8")

if pretty != files["dispatch_target"].read_bytes():
    fail("DISPATCH_TARGET_NOT_EXACT_DERIVATION")

if hashlib.sha256(canonical).hexdigest() != \
   "2333c2521db84ddb347b23a956acebdc6ad713c61cc890b76d7b04d0b8d2fc7f":
    fail("DISPATCH_CANONICAL_SHA")

if dst["dispatch"]["2.0.0"][
    "eligible_only_after_separate_reviewed_activation"
] is not True:
    fail("DISPATCH_SEPARATE_ACTIVATION_FLAG")

if dst["unsupported_or_missing_schema_version"] != "REJECT":
    fail("DISPATCH_REJECT_POLICY")

if dst[
    "heuristic_fallback_between_schema_versions"
] is not False:
    fail("DISPATCH_HEURISTIC_FALLBACK")

dd = json.loads(
    files["dispatch_diff"].read_text(
        encoding="utf-8"
    )
)

if dd["exact_delta_count"] != 1:
    fail("DISPATCH_DELTA_COUNT")

if dd["changes"] != [
    {
        "from":
            "REVIEW_CANDIDATE_NOT_ACTIVE",

        "json_path":
            "$.status",

        "to":
            "ACTIVE_UPON_EXPLICIT_SCHEMA_V2_ACTIVATION_DECISION"
    }
]:
    fail("DISPATCH_DELTA_CONTENT")

if dd["all_other_json_values_identical"] is not True:
    fail("DISPATCH_PRESERVATION")

if dd["future_active_path"] != \
   "config/protocol_specification_schema_version_dispatch.v1.json":
    fail("ACTIVE_DISPATCH_PATH")

if dd["future_active_path_created_by_package"] is not False:
    fail("PREMATURE_DISPATCH_CREATION")

# Reconstruct exact successor target.
text = files["successor_source"].read_text(
    encoding="utf-8"
).replace("\r\n", "\n").replace("\r", "\n")

sd = json.loads(
    files["successor_diff"].read_text(
        encoding="utf-8"
    )
)

if sd["exact_transformation_count"] != 3:
    fail("SUCCESSOR_TRANSFORMATION_COUNT")

if len(sd["transformations"]) != 3:
    fail("SUCCESSOR_TRANSFORMATION_LENGTH")

expected_ids = [
    "TITLE",
    "STATUS",
    "ACTIVATION_BLOCK",
]

if [
    x["id"]
    for x in sd["transformations"]
] != expected_ids:
    fail("SUCCESSOR_TRANSFORMATION_IDS")

for item in sd["transformations"]:
    old = item["from"]
    new = item["to"]

    if text.count(old) != 1:
        fail(
            "SUCCESSOR_SOURCE_COUNT|"
            + item["id"]
        )

    text = text.replace(
        old,
        new,
        1
    )

raw = text.encode("utf-8")

if raw != files["successor_target"].read_bytes():
    fail("SUCCESSOR_TARGET_NOT_EXACT_DERIVATION")

if sd["all_other_text_byte_preserved"] is not True:
    fail("SUCCESSOR_PRESERVATION")

if sd[
    "decision_0019_historical_file_modified"
] is not False:
    fail("DECISION_0019_MUTATION")

if sd[
    "operative_before_later_explicit_activation"
] is not False:
    fail("SUCCESSOR_PREMATURE_OPERATION")

# Validate authorization.
auth = json.loads(
    files["authorization"].read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
   "AUTHORIZED_TO_AUTHOR_SCHEMA_V2_ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_ONLY":
    fail("AUTHORIZATION_STATUS")

if auth[
    "proposed_active_version_dispatch_form"
]["expected_file_sha256"] != expected_sha["dispatch_target"]:
    fail("AUTH_DISPATCH_TARGET")

if auth[
    "proposed_active_decision_0019_successor_form"
]["expected_file_sha256"] != expected_sha["successor_target"]:
    fail("AUTH_SUCCESSOR_TARGET")

if set(
    auth["mandatory_review_requirements"]
) != {
    f"AF{i:02d}"
    for i in range(1, 11)
}:
    fail("AF_AUTHORIZATION_SET")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

# Validate historical repository binding copied into package.
binding = json.loads(
    files["binding"].read_text(
        encoding="utf-8"
    )
)

if binding["checkpoint_commit"] != \
   "6eba8a1fc69c0b1146e033b031f5948a245bd84b":
    fail("BINDING_COMMIT")

if binding["checkpoint_tree"] != \
   "67a80e37f8c94c2c5878f4ddde4da1943e7a5dc6":
    fail("BINDING_TREE")

state = binding["authoring_checkpoint_state"]

for key in (
    "active_v2_hash_contract_absent",
    "active_version_dispatch_policy_absent",
    "curl_json_absent",
):
    if state[key] is not True:
        fail("BINDING_ABSENCE|" + key)

for key in (
    "schema_v2_activated",
    "decision_0019_successor_adopted",
    "positive_v4_to_v2_mapping_defined",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if state[key] is not False:
        fail("BINDING_NONACTIVATION|" + key)

blob_map = {
    "reviewed_version_dispatch":
        files["dispatch_source"],

    "reviewed_decision_0019_successor":
        files["successor_source"],

    "approved_v2_hash_active_form":
        files["hash_form"],

    "hash_active_form_human_approval_record":
        files["hash_approval"],

    "decision_0061_authorization":
        files["authorization"],

    "schema_v2":
        files["schema_v2"],

    "v1_hash_contract":
        files["v1_hash"],

    "decision_0019":
        files["decision_0019"],

    "zlib":
        files["zlib"],

    "libpcap":
        files["libpcap"],
}

repo_artifacts = binding["repository_artifacts"]

for key, path in blob_map.items():
    expected_blob = repo_artifacts[key]["git_blob"]
    actual_blob = git_blob_sha1(
        path.read_bytes()
    )

    if actual_blob != expected_blob:
        fail("GIT_BLOB|" + key)

# AF matrix.
matrix = files["matrix"].read_text(
    encoding="utf-8"
)

for i in range(1, 11):
    if f"## AF{i:02d}" not in matrix:
        fail("MATRIX_AF|" + str(i))

# Blank review packet is intentionally synthetic only as a blank template.
review = files["review"].read_text(
    encoding="utf-8"
).replace("\r\n", "\n").replace("\r", "\n")

for i in range(1, 11):
    rid = f"AF{i:02d}"

    heading = re.search(
        r"^##\s+" + rid + r"\b.*$",
        review,
        re.M
    )

    if not heading:
        fail("REVIEW_HEADING|" + rid)

    tail = review[heading.end():]
    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = (
        tail[:nxt.start()]
        if nxt
        else tail
    )

    values = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if values != [""]:
        fail(
            "REVIEW_NOT_BLANK|"
            + rid
            + "|"
            + repr(values)
        )

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    review,
    re.M
)

if overall != [""]:
    fail("OVERALL_NOT_BLANK")

for label in (
    "Human reviewer role",
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    values = re.findall(
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        review,
        re.M
    )

    if values != [""]:
        fail("REVIEWER_IDENTITY_NOT_BLANK|" + label)

# Package manifest integrity.
manifest = json.loads(
    files["manifest"].read_text(
        encoding="utf-8"
    )
)

if manifest["package_id"] != \
   "SVF-SCHEMA-V2-ACTIVATION-ARTIFACT-FINALIZATION-PACKAGE-V1":
    fail("MANIFEST_ID")

for entry in manifest["files"]:
    p = here / entry["name"]

    if not p.is_file():
        fail("MANIFEST_FILE_MISSING|" + entry["name"])

    if sha(p) != entry["sha256"]:
        fail("MANIFEST_SHA|" + entry["name"])

    if p.stat().st_size != entry["size_bytes"]:
        fail("MANIFEST_SIZE|" + entry["name"])

expected_file_set = {
    entry["name"]
    for entry in manifest["files"]
}

expected_file_set.update({
    "21_schema_v2_activation_artifact_finalization_package_manifest.v1.json",
    "22_schema_v2_activation_artifact_finalization_package.v1.SHA256SUMS",
})

actual_file_set = {
    p.name
    for p in here.iterdir()
    if p.is_file()
}

if actual_file_set != expected_file_set:
    fail(
        "PACKAGE_FILE_SET|"
        + repr(
            sorted(
                actual_file_set
                ^ expected_file_set
            )
        )
    )

print("REVIEWED_VERSION_DISPATCH_SOURCE_BINDING=PASS")
print("ACTIVE_FORM_VERSION_DISPATCH_EXACT_DELTA_COUNT=1")
print("ACTIVE_FORM_VERSION_DISPATCH_SHA256=67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee")
print("ACTIVE_FORM_VERSION_DISPATCH_CANONICAL_JSON_SHA256=2333c2521db84ddb347b23a956acebdc6ad713c61cc890b76d7b04d0b8d2fc7f")
print("REVIEWED_DECISION_0019_SUCCESSOR_SOURCE_BINDING=PASS")
print("ACTIVE_FORM_DECISION_0019_SUCCESSOR_EXACT_TRANSFORMATION_COUNT=3")
print("ACTIVE_FORM_DECISION_0019_SUCCESSOR_SHA256=a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb")
print("APPROVED_V2_HASH_ACTIVE_FORM_BINDING=PASS")
print("DECISION_0019_HISTORICAL_IMMUTABILITY_BOUND=YES")
print("AF01_TO_AF10_PRESENT=PASS")
print("AF01_TO_AF10_REVIEW_DECISIONS_INITIAL_STATE=BLANK")
print("ACTIVATION_ARTIFACT_FINALIZATION_OVERALL_DECISION_INITIAL_STATE=BLANK")
print("ACTIVATION_ARTIFACT_REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("SYNTHETIC_HUMAN_DECISION=NO")
print("SELF_CONTAINED_ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_VERIFICATION=PASS")
